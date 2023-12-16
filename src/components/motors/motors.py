import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sensors')))
from sensors import GPIO as gpio
import RPi.GPIO as GPIO   
from time import sleep

class MotorsDriver:
    def __init__(self, gpio):
        self.gpio = gpio

        GPIO.setmode(GPIO.BOARD)
        
        GPIO.setup(self.gpio['motor-left']['in1'],GPIO.OUT)
        GPIO.setup(self.gpio['motor-left']['in2'],GPIO.OUT)
        
        GPIO.setup(self.gpio['motor-right']['in1'],GPIO.OUT)
        GPIO.setup(self.gpio['motor-right']['in2'],GPIO.OUT)

        
        GPIO.setup(self.gpio['motor-left']['pwm'],GPIO.OUT)
        GPIO.setup(self.gpio['motor-right']['pwm'],GPIO.OUT)
        
   
        GPIO.output(self.gpio['motor-left']['in1'],GPIO.LOW)
        GPIO.output(self.gpio['motor-left']['in2'],GPIO.LOW)
        
        GPIO.output(self.gpio['motor-right']['in1'],GPIO.LOW)
        GPIO.output(self.gpio['motor-right']['in2'],GPIO.LOW)

        self.left_motor_speed=GPIO.PWM(self.gpio['motor-left']['pwm'],1000)
        
        self.right_motor_speed=GPIO.PWM(self.gpio['motor-right']['pwm'],1000)
        
        self.left_motor_speed.start(self.gpio['motor-right']['pwm'])
        
        self.right_motor_speed.start(self.gpio['motor-left']['pwm'])
        
    def forward(self):
        GPIO.output(self.gpio['motor-left']['in1'],GPIO.LOW)
        GPIO.output(self.gpio['motor-left']['in2'],GPIO.HIGH)
        GPIO.output(self.gpio['motor-right']['in1'],GPIO.HIGH)
        GPIO.output(self.gpio['motor-right']['in2'],GPIO.LOW)

    def backward(self):
        GPIO.output(self.gpio['motor-left']['in1'],GPIO.HIGH)
        GPIO.output(self.gpio['motor-left']['in2'],GPIO.LOW)
        GPIO.output(self.gpio['motor-right']['in1'],GPIO.LOW)
        GPIO.output(self.gpio['motor-right']['in2'],GPIO.HIGH)

    def left(self):
        GPIO.output(self.gpio['motor-left']['in1'],GPIO.HIGH)
        GPIO.output(self.gpio['motor-left']['in2'],GPIO.LOW)
        GPIO.output(self.gpio['motor-right']['in1'],GPIO.HIGH)
        GPIO.output(self.gpio['motor-right']['in2'],GPIO.LOW)

    def right(self):
        GPIO.output(self.gpio['motor-left']['in1'],GPIO.LOW)
        GPIO.output(self.gpio['motor-left']['in2'],GPIO.HIGH)
        GPIO.output(self.gpio['motor-right']['in1'],GPIO.LOW)
        GPIO.output(self.gpio['motor-right']['in2'],GPIO.HIGH)

    def stop(self):
        GPIO.output(self.gpio['motor-left']['in1'],GPIO.LOW)
        GPIO.output(self.gpio['motor-left']['in2'],GPIO.LOW)
        GPIO.output(self.gpio['motor-right']['in1'],GPIO.LOW)
        GPIO.output(self.gpio['motor-right']['in2'],GPIO.LOW)

    def low(self):
        self.left_motor_speed.ChangeDutyCycle(25)
        self.right_motor_speed.ChangeDutyCycle(25)

    def medium(self):
        self.left_motor_speed.ChangeDutyCycle(50)
        self.right_motor_speed.ChangeDutyCycle(50)

    def high(self):
        self.left_motor_speed.ChangeDutyCycle(75)
        self.right_motor_speed.ChangeDutyCycle(75)
        
    def cleanup(self):
        GPIO.cleanup()