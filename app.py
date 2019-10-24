#!/usr/bin/env python3

import time
import logging
import configparser
import io
import requests
#import picamera
#import RPi.GPIO as GPIO

PIR_PIN = 7
STEPPER_PINS = [31, 33, 35, 37]

#  Vars
#picam = picamera.PiCamera()
config = configparser.ConfigParser()

def config_gpio():
    logging.info("GPIO configuration")
    #GPIO.setwarnings(True)
    #GPIO.setmode(GPIO.BOARD)

def config_pir():
    logging.info("PIR configuration")
    #GPIO.setup(PIR_PIN, GPIO.IN)
    #GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion_detected)

def config_motor():
    logging.info("Motor configuration")
    #for pin in STEPPER_PINS:
    #    GPIO.setup(pin, GPIO.OUT)
    #    GPIO.output(pin, 0)

def get_image():
    logging.info("Getting image...")
    #picam.start_preview()
    time.sleep(2)  # warmup camera
    my_stream = io.BytesIO()
    #picam.capture(my_stream, 'jpeg')
    #picam.stop_preview()
    logging.info("Image data ready.")
    return my_stream

def process_image(img_data):
    logging.info("Processing image...")
    # Request
    headers = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': config["AZURE"]["api_key"]}
    params = {'visualFeatures': 'Categories,Description'}
    response = requests.post(url=config["AZURE"]["server"], headers=headers, params=params, data=img_data)
    # Process return value
    logging.info("Response code = %d", response.status_code)
    if response.status_code == 200:
        logging.debug(response.text)
        json_res = response.json()
        tags = json_res["description"]["tags"]
        if config["DEFAULT"]["animal_detect"] in tags:
            return True
    return False

def motion_detected(gpio_pin):
    logging.info("Motion Detected!")

#  Main
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s (%(lineno)d): %(message)s', level=logging.DEBUG)
config.read('app.ini')

#data = open('atari.jpg', 'rb').read()
#process_image(data)

try:
    logging.info("SmartFeederApp started")
    while 1:
        time.sleep(1)
        logging.debug("Waiting...")
except KeyboardInterrupt:
        logging.info("Closing...")
        #GPIO.cleanup()
        # picam.close()
        logging.info("Bye")


#while True:
#    i=GPIO.input(PIR_PIN)
#    if i==0:                 #When output from motion sensor is LOW
#        print("No intruders")
#    elif i==1:               #When output from motion sensor is HIGH
#        print("Intruder detected")
#   time.sleep(0.5)
