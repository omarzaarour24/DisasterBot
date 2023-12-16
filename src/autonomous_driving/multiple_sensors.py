import time
import RPi.GPIO as GPIO
from ultrasonicsensor import ultrasonicRead

TRIGB = 11
ECHOB = 13

TRIGF = 38
ECHOF = 40

TRIGL = 21
ECHOL = 23

TRIGR = 15
ECHOR = 10

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(TRIGB, GPIO.OUT)
GPIO.setup(ECHOB, GPIO.IN)

GPIO.setup(TRIGF, GPIO.OUT)
GPIO.setup(ECHOF, GPIO.IN)

GPIO.setup(TRIGR, GPIO.OUT)
GPIO.setup(ECHOR, GPIO.IN)


GPIO.setup(ECHOL, GPIO.IN)
GPIO.setup(TRIGL, GPIO.OUT)

distance = 0
distance2 = 0
distance3 = 0
distance4 = 0

try:
    while True:
        print("distance: "+str(distance)+" | " + str(distance2)+" | "+str(distance3)+" | " + str(distance4))
        time.sleep(0.2)
        distance = ultrasonicRead(GPIO, TRIGB, ECHOB)
        time.sleep(0.2)
        distance2 = ultrasonicRead(GPIO, TRIGF, ECHOF)
        time.sleep(0.2)
        distance3 = ultrasonicRead(GPIO, TRIGR, ECHOR)
        time.sleep(0.2)
        distance4 = ultrasonicRead(GPIO, TRIGL, ECHOL)
        time.sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()



