from rpi_hardware_pwm import HardwarePWM
import time

pwm = HardwarePWM(pwm_channel=0, hz=60)
pwm.start(100) # full duty cycle

pwm.change_duty_cycle(7)
pwm.change_frequency(50)
count = 4
while True:
    count = (count+0.1)%10
    print(count)
    time.sleep(0.01)
    pwm.change_duty_cycle(count)

pwm.stop()
