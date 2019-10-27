#!/usr/bin/env python3

import time
import logging
import configparser
import io
import requests
import picamera
import RPi.GPIO as GPIO

PIR_PIN = 7
STEPPER_PINS = [31, 33, 35, 37]
LED_PIN = 11
IMG_NAME = "/tmp/img.jpg"

#  Vars
config = configparser.ConfigParser()

def config_gpio():
    logging.info("GPIO configuration")
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BOARD)

    logging.info("PIR configuration")
    GPIO.setup(PIR_PIN, GPIO.IN)
    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion_detected)

    logging.info("Motor configuration")
    for pin in STEPPER_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

    logging.info("IR configuration")
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, 0)

def get_image():
    logging.info("Getting image...")
    cam = picamera.PiCamera()
    cam.resolution = (1024, 768)
    GPIO.output(LED_PIN, 1)
    cam.start_preview()
    
    time.sleep(1)
    my_stream = io.BytesIO()
    cam.capture(my_stream, format='jpeg')
    my_stream.seek(0)
    
    cam.stop_preview()
    GPIO.output(LED_PIN, 0)
    cam.close()
    logging.info("Image data ready.")
    
    return my_stream

def process_image(img_data):
    if img_data:
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
    else:
        logging.error("img_data is empty")
        return False

def close():
    GPIO.cleanup()

def motion_detected(gpio_pin):
    logging.info("Motion Detected!")
    ret = process_image(get_image())
    if ret:
        logging.warning("%s detected!", config["DEFAULT"]["animal_detect"])
    else:
        logging.info("%s NOT detected", config["DEFAULT"]["animal_detect"])

#  Main
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s (%(lineno)d): %(message)s', level=logging.DEBUG)
config.read('app.ini')
config_gpio()

#data = open('atari.jpg', 'rb').read()
#process_image(data)

try:
    logging.info("SmartFeederApp started")
    while 1:
        time.sleep(100)
        logging.debug("Waiting...")
except KeyboardInterrupt:
        logging.info("Closing...")
        close()
        logging.info("Bye")
