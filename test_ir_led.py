#!/usr/bin/env python3

import time
import logging
import configparser
import io
import RPi.GPIO as GPIO

LED_PIN = 11

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(LED_PIN, GPIO.OUT)

GPIO.output(LED_PIN, 1)
time.sleep(10)
GPIO.output(LED_PIN, 0)

GPIO.cleanup()
