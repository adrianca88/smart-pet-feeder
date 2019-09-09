#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

PIR_PIN = 7

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_PIN, GPIO.IN)

def MOTION(PIR_PIN):
    print ("Motion Detected!")

try:
    print("Starting PIR test app")
    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=MOTION)
    while 1:
        time.sleep(100)
except KeyboardInterrupt:
        print("Bye!")
        GPIO.cleanup()


#while True:
#    i=GPIO.input(PIR_PIN)
#    if i==0:                 #When output from motion sensor is LOW
#        print("No intruders")
#    elif i==1:               #When output from motion sensor is HIGH
#        print("Intruder detected")
#   time.sleep(0.5)
