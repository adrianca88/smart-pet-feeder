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
IMG_NAME = "/tmp/img.jpg"

#  Vars
cam = picamera.PiCamera()
config = configparser.ConfigParser()

def config_gpio():
    logging.info("GPIO configuration")
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BOARD)

def config_pir():
    logging.info("PIR configuration")
    GPIO.setup(PIR_PIN, GPIO.IN)
    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion_detected)

def config_motor():
    logging.info("Motor configuration")
    for pin in STEPPER_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

def config_cam():
    logging.info("Camera configuration")
    #cam = picamera.PiCamera()

def get_image():
    if cam:
        logging.info("Getting image...")
        cam.start_preview()
        time.sleep(2)  # warmup camera
        #my_stream = io.BytesIO()
        #cam.capture(my_stream, 'jpeg')
        cam.capture(IMG_NAME)
        cam.stop_preview()
        logging.info("Image data ready.")
        #return my_stream
        return True
    else:
        logging.error("Camera not ready")
        #return None
        return False

#def process_image(img_data):
def process_image(img_path):
    #if img_data:
    if img_path:
        logging.info("Processing image...")
        # Request
        headers = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': config["AZURE"]["api_key"]}
        params = {'visualFeatures': 'Categories,Description'}
        data = open(img_path, 'rb').read()
        response = requests.post(url=config["AZURE"]["server"], headers=headers, params=params, data=data)
        # Process return value
        logging.info("Response code = %d", response.status_code)
        if response.status_code == 200:
            logging.debug(response.text)
            json_res = response.json()
            tags = json_res["description"]["tags"]
            logging.debug(tags)
            logging.debug(config["DEFAULT"]["animal_detect"])
            if config["DEFAULT"]["animal_detect"] in tags:
                return True
        return False
    else:
        logging.error("img_data is empty")
        return False

def close():
    GPIO.cleanup()
    if cam: 
        cam.close()

def motion_detected(gpio_pin):
    logging.info("Motion Detected!")
    ret = False
    if get_image():
        ret = process_image(IMG_NAME)
    #ret = process_image(get_image())
    if ret:
        logging.warning("%s detected!", config["DEFAULT"]["animal_detect"])
    else:
        logging.info("%s NOT detected", config["DEFAULT"]["animal_detect"])

#  Main
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s (%(lineno)d): %(message)s', level=logging.DEBUG)

#config = configparser.ConfigParser()
config.read('app.ini')

config_gpio()
config_pir()
config_cam()
#config_motor()

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


#while True:
#    i=GPIO.input(PIR_PIN)
#    if i==0:                 #When output from motion sensor is LOW
#        print("No intruders")
#    elif i==1:               #When output from motion sensor is HIGH
#        print("Intruder detected")
#   time.sleep(0.5)
