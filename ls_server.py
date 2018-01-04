#!/usr/bin/env python

from flask import Flask, render_template, request, jsonify, abort, make_response
import time
from threading import Thread
import os
from crontab import CronTab
import signal
import sys
from flask_restful import Resource, Api
import json
from switch_hardware import server


DEBUG = False
pid_file_name = 'ls_server_pid'


app = Flask(__name__)
api = Api(app)


_API_URL_ROUTE = '/api/v1.0/'

switch = server.outletswitch.OutletSwitch()

class LightSwitchAPI(Resource):
    def __init__(self):
        self.switch = switch = server.outletswitch.OutletSwitch()

    def get(self):
        try:
            return { 'status' : self.switch.get_status() }
        except:
            return { 'message' : 'ERROR: failed to get switch status' }, 400

    def put(self):
        if not request.is_json:
            return { 'message' : 'Data provided must be in JSON format.' }, 400

        data = json.loads(request.data)
        try:
            self.switch.set_status(data['status'])
        except:
            return { 'message' : 'ERROR: failed to set switch status' }, 400

        return { 'status' : data['status'] }

api.add_resource(LightSwitchAPI, _API_URL_ROUTE + 'light_status')


@app.route("/")
def light_main():
    return render_template('main.html')


if __name__ == "__main__":
    port = 3333
    try:
        port = int(sys.argv[1])
    except IndexError:
        pass

    try:
        app.run(host='0.0.0.0', port=port, debug=DEBUG)
    except KeyboardInterrupt:
        pass

    print 'light switch server shutting down...'
