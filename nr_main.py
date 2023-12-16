import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src','communication', 'mosquitto')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src','manual_controls')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src','components')))
from dotenv import dotenv_values
import time
from sensors import GPIO as gpio
from topics import sensors as sensor_topics
from topics import notopics as closed_topics
from topics import commands as command_topics
import subMQTT as mqtt
from radar.radar import RadarDriverWithMQTT
from motors.motors import MotorsDriver

motors_driver = MotorsDriver(gpio)
motors_driver.high()
def interpret_command(topic,payload):
        dp = payload.decode('utf-8')
        if command_topics['motor']['manual_controls'] in topic:
            if dp == 'forward':
                motors_driver.forward()
            elif dp == 'backward':
                motors_driver.backward()
            elif dp == 'left':
                motors_driver.left()
            elif dp == 'right':
                motors_driver.right()
            elif dp == 'stop':
                motors_driver.stop()
        if command_topics['enable']['camera'] in topic:
            if dp == 'enabled':
                print(payload)
            elif dp == 'disabled':
                print(payload)
        if command_topics['enable']['auto_drive'] in topic:
           if dp == 'enabled':
                print(payload)
           elif dp == 'disabled':
                print(payload)
        if command_topics['enable']['radar'] in topic:
           if dp == 'enabled':
                print(payload)
           elif dp == 'disabled':
                print(payload)

env_vars = dotenv_values()
BROKER_ADDRESS = env_vars['BROKER_ADDRESS']
PORT = int(env_vars['PORT'])
client = mqtt.MQTTSubscriber(BROKER_ADDRESS, PORT, "native-robot", command_topics, interpret_command)
client.connect()
radarDriver = RadarDriverWithMQTT(gpio, client, sensor_topics['sensors']['radar'])
radarDriver.start_radar()


