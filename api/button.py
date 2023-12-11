import RPi.GPIO as GPIO
from time import sleep
#Set warnings off (optional)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#Set Button and LED pins
Button = 7
#Setup Button and LED
GPIO.setup(Button,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#flag = 0

while True:
    button_state = GPIO.input(Button)
    print(button_state)
    if button_state == 0:
        print('push')
    else:
        print('no push')
    sleep(1)