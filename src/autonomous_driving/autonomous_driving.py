import RPi.GPIO as GPIO
from ultrasonicsensor import ultrasonicRead

ena = 18
enb = 16
in1 = 23
in2 = 24
in3 = 25
in4 = 12
temp1=1

TRIGB=3
ECHOB=5
TRIGL=7
ECHOL=11
TRIGR=13
ECHOR=15

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
GPIO.setup(TRIGB, GPIO.OUT)
GPIO.setup(ECHOB, GPIO.IN)
GPIO.setup(TRIGR, GPIO.OUT)
GPIO.setup(ECHOR, GPIO.IN)
GPIO.setup(TRIGL, GPIO.OUT)
GPIO.setup(ECHOL, GPIO.IN)

distanceBack = ultrasonicRead(GPIO, TRIGB, ECHOB)
distanceRight = ultrasonicRead(GPIO, TRIGR, ECHOR)
distanceLeft = ultrasonicRead(GPIO, TRIGL, ECHOL)

ena=GPIO.PWM(ena,1000)
enb=GPIO.PWM(enb,1000)
ena.start(18)
enb.start(16)

while ():

    if distanceRight < 50:
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)

    elif distanceLeft < 50:
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.HIGH)

    elif distanceBack < 50:
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)
