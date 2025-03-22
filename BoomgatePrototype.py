import RPi.GPIO as GPIO # type: ignore
from time import sleep



GPIO.setmode(GPIO.BCM)

GPIO.setup(13, GPIO.OUT)
pwm = GPIO.PWM(13, 50)
on = GPIO.output(13, True)
off = GPIO.output(13, False)
pwm.start(0)

GPIO.setup(6, GPIO.IN)
#https://automaticaddison.com/how-to-make-a-line-following-robot-using-raspberry-pi/ (Line Sensor Section)


def Open_Close():
    
    print("Opening")
    
    on
    pwm.ChangeDutyCycle(7)
    sleep(0.5)
    off
    pwm.ChangeDutyCycle(0)
    print("Waiting")
    sleep(3)
    
    on
    pwm.ChangeDutyCycle(2.5)
    sleep(0.5)
    off
    pwm.ChangeDutyCycle(0)

while True:
    if(GPIO.input(6) == False):
        Open_Close()
        break
    else:
        sleep(0.2)

pwm.stop()
GPIO.cleanup()