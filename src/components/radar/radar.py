import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ultrasonic')))
import RPi.GPIO as GPIO
from time import sleep
import time
from threading import Thread
import socket
from rpi_hardware_pwm import HardwarePWM
from ultrasonic import ultrasonicRead


class RadarDriverWithSockets:
    def __init__(self, sensors, address, port):
        self.current_angle = 0
        self.current_distance = 0

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(sensors['forward-ultrasonic']['trig'], GPIO.OUT)
        GPIO.setup(sensors['forward-ultrasonic']['echo'], GPIO.IN)

        self.servo = HardwarePWM(pwm_channel=1, hz=60)
        self.servo.start(100)

        self.server_address = (address, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)
        print("Connected to the server.")

    def start_radar(self):
        try:
            sensor_thread = Thread(target=self.sensor, daemon=True)
            servo_thread = Thread(target=self.servo_rotation, daemon=True)

            sensor_thread.start()
            servo_thread.start()

            sensor_thread.join()
            servo_thread.join()

        except KeyboardInterrupt:
            self.cleanup()

    def sensor(self):
        try:
            while True:
                distance = ultrasonicRead(GPIO, 
                                          self.sensors['forward-ultrasonic']['trig'], 
                                          self.sensors['forward-ultrasonic']['echo'])
                self.current_distance = distance
        except KeyboardInterrupt:
            self.cleanup()

    def servo_rotation(self):
        try:
            while True:
                for angle in range(0, 180, 2):
                    angle = 180 - angle
                    self.servo.change_duty_cycle(float(2 + (angle / 18)))
                    time.sleep(0.01)
                    self.servo.change_duty_cycle(0)
                    self.current_angle = angle
                    packet = str("{:05.2f}".format(self.current_distance)) + str("{:03d}".format(self.current_angle))
                    self.client_socket.send(packet.encode())
                for angle in range(180, 0, -2):
                    angle = 180 - angle
                    self.servo.change_duty_cycle(float(2 + (angle / 18)))
                    time.sleep(0.01)
                    self.servo.change_duty_cycle(0)
                    self.current_angle = angle
                    packet = str("{:05.2f}".format(self.current_distance)) + str("{:03d}".format(self.current_angle))
                    self.client_socket.send(packet.encode())

        except KeyboardInterrupt:
            self.cleanup()

    def cleanup(self):
        self.servo.stop()
        GPIO.cleanup()
        sys.exit(0)
        
class RadarDriverWithMQTT:
    def __init__(self, gpio_sensors, mqtt_client, radar_topic):
        self.mqtt_client = mqtt_client
        self.gpio_sensors = gpio_sensors
        self.radar_topic = radar_topic

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.gpio_sensors['forward-ultrasonic']['trig'], GPIO.OUT)
        GPIO.setup(self.gpio_sensors['forward-ultrasonic']['echo'], GPIO.IN)

        self.servo = HardwarePWM(pwm_channel=1, hz=60)
        self.servo.start(100)

    def start_radar(self):
        try:
            while True:
                for angle in range(0, 180, 2):
                    angle = 180 - angle
                    self.servo.change_duty_cycle(float(2 + (angle / 18)))
                    time.sleep(0.01)
                    self.servo.change_duty_cycle(0)
                    distance = ultrasonicRead(GPIO, 
                                              self.gpio_sensors['forward-ultrasonic']['trig'], 
                                              self.gpio_sensors['forward-ultrasonic']['echo'])
                    packet = "{:.2f}{:03d}".format(distance, angle)
                    self.mqtt_client.publish(self.radar_topic, packet)
                for angle in range(180, 0, -2):
                    angle = 180 - angle
                    self.servo.change_duty_cycle(float(2 + (angle / 18)))
                    time.sleep(0.01)
                    self.servo.change_duty_cycle(0)
                    distance = ultrasonicRead(GPIO, 
                                              self.gpio_sensors['forward-ultrasonic']['trig'], 
                                              self.gpio_sensors['forward-ultrasonic']['echo'])
                    packet = "{:.2f}{:03d}".format(distance, angle)
                    self.mqtt_client.publish(self.radar_topic, packet)

        except KeyboardInterrupt:
            self.cleanup()

    def cleanup(self):
        self.servo.stop()
        GPIO.cleanup()
        sys.exit(0)
        

# BROKER_ADDRESS = "192.168.43.145"
# BROKER_PORT = 1883
# client = mqtt.MQTTSubscriber(BROKER_ADDRESS, BROKER_PORT, "pub", closed_topics)
# client.connect()
# radarDriver = RadarDriverWithMQTT(sensor_gpio, client, sensor_topics['sensors']['radar'])
# radarDriver.start_radar()

