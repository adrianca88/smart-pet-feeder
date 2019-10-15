#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import picamera

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)

# PIR
PIR_PIN = 7
GPIO.setup(PIR_PIN, GPIO.IN)

# MOTOR
STEPPER_PINS = [31,33,35,37]

for pin in STEPPER_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# CAMERA
picam = picamera.PiCamera()

# CODE
def _get_image():
    picam.start_preview()
    time.sleep(1)
    picam.capture('test.jpg')
    picam.stop_preview()
    picam.close()


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
