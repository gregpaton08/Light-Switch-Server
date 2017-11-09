#!/usr/bin/env python

from flask import Flask, render_template, request, jsonify, abort, make_response
import time
import lightswitch
from threading import Thread
import os
from crontab import CronTab
import signal
import sys
import lsauth
import pidfile
from flask_restful import Resource, Api
import json


_PORT = 3333
DEBUG = True
pid_file_name = 'ls_server_pid'


app = Flask(__name__)
api = Api(app)


_API_URL_ROUTE = '/api/v1.0/'

light_switch = lightswitch.LightSwitch()

class LightSwitchAPI(Resource):
    def __init__(self):
        self.light_switch = lightswitch.LightSwitch()

    def put(self):
        if not request.is_json:
            return { 'message' : 'Data provided must be in JSON format.' }, 400

        data = json.loads(request.data)
        self.light_switch.set_light(data['status'])

        return { 'status' : data['status'] }

api.add_resource(LightSwitchAPI, _API_URL_ROUTE + 'light_status')


@app.route("/")
def light_main():
    return render_template('main.html')


if __name__ == "__main__":
    pid_file = pidfile.PidFile(pid_file_name)

    try:
        app.run(host='0.0.0.0', port=_PORT, debug=DEBUG)
    except KeyboardInterrupt:
        pass

    light_switch.cleanup()
    pid_file.cleanup()
    print 'light switch server shutting down...'
