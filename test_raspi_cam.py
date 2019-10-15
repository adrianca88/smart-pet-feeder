#!/usr/bin/env python3

import time
import picamera

picam = picamera.PiCamera()
picam.start_preview()
time.sleep(5)
picam.capture('test.jpg')
picam.stop_preview()
picam.close()

