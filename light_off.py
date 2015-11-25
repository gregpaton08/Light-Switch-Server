#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import ls

GPIO.setmode(GPIO.BCM)
GPIO.setup(ls.GPIO_LIGHT_OFF, GPIO.OUT)
GPIO.output(ls.GPIO_LIGHT_OFF, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(ls.GPIO_LIGHT_OFF, GPIO.LOW)
GPIO.cleanup(ls.GPIO_LIGHT_OFF)
