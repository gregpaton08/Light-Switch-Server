#!/usr/bin/env python

from flask import Flask, render_template, request, jsonify, abort, make_response
import RPi.GPIO as GPIO
import time
import lightswitch
from threading import Thread
import os
from crontab import CronTab
import signal
import sys
import lsauth
import lsswitches
import ls
import pidfile

app = Flask(__name__)

light_switch = lightswitch.LightSwitch()

_PORT = 3333
DEBUG = True
pid_file_name = 'ls_server_pid'

@app.route("/")
@lsauth.requires_auth
def light_main():
    return render_template('main.html')


@app.route("/light_on")
@lsauth.requires_auth
def light_on():
    light_switch.set_light(True)
    return render_template('main.html')


@app.route("/light_off")
@lsauth.requires_auth
def light_off():
    light_switch.set_light(False)
    return render_template('main.html')


@app.route("/light_auth")
@lsauth.requires_auth
def light_auth():
    return render_template('main.html')


if __name__ == "__main__":
    pid_file = pidfile.PidFile(pid_file_name)

    try:
        app.run(host='0.0.0.0', port=_PORT, debug=DEBUG)
    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
    pid_file.cleanup()
    print 'light switch server shutting down...'
