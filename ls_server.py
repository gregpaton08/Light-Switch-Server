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
DAYS_OF_WEEK = [
    'Sunday',
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
]

_URL_ROUTE = '/switches/API/v1.0/switches'

@app.route(_URL_ROUTE, methods=['POST'])
def add_switch():
    # Make sure the request contains JSON
    if not request.json:
        return jsonify({'error' : 'no json found'}), 400

    # Grab the relevant data from the request and add the new switch
    switch = {
        'room'   : request.json.get('room',   u''),
        'device' : request.json.get('device', u''),
        'status' : request.json.get('status', False),
    }
    lsswitches.add_switch(switch)

    return jsonify({'switch': switch}), 201


@app.route(_URL_ROUTE + '/<int:switch_id>', methods=['DELETE'])
def delete_switch(switch_id):
    if lsswitches.delete_switch(switch_id):
        return jsonify({'result': True})

    return jsonify({'error' : 'no switch for id ' + str(switch_id)}), 400


@app.route(_URL_ROUTE, methods=['GET'])
def route():
    switches = lsswitches.get_switches()
    return jsonify({'switches' : switches})


@app.route(_URL_ROUTE + '/<int:switch_id>', methods=['PUT'])
def update_switch(switch_id):
    # Get the switch
    switches = lsswitches.get_switches()
    switch = [switch for switch in switches if switch['id'] == switch_id]
    if 0 == len(switch):
        return jsonify({'error' : 'no switch for id ' + str(switch_id)}), 400

    if not request.json:
        abort(400)
    if 'status' in request.json:
        if type(request.json['status']) is not bool:
            abort(400)
        else:
            light_switch.set_light(request.json['status'])
    switch[0]['status'] = request.json.get('status', switch[0]['status'])
    
    return jsonify({'switch': switch[0]}), 201


@app.route(_URL_ROUTE + '/<int:switch_id>/status', methods=['GET'])
def get_switch_status(switch_id):
    # Get the switch
    switches = lsswitches.get_switches()
    switch = [switch for switch in switches if switch['id'] == switch_id]
    if 0 == len(switch):
        return jsonify({'error' : 'no switch for id ' + str(switch_id)}), 400
    switch = switch[0]

    return jsonify({'status' : switch['status']}), 201

@app.route(_URL_ROUTE + '/<int:switch_id>/toggle', methods=['PUT'])
def toggle_switch(switch_id):
    switches = lsswitches.get_switches()
    switch = [switch for switch in switches if switch['id'] == switch_id]
    if 1 != len(switch):
        return jsonify({'error' : 'switch with id ' + str(switch_id) + ' does not exist'}), 400
    switch = switch[0]

    # Toggle the switch status
    switch['status'] = not switch['status']

    # Update the light status
    light_switch.set_light(switch['status'])

    if not lsswitches.update_switch(switch):
        return jsonify({'error' : 'switch with id ' + str(switch_id) + ' does not exist'}), 400

    return jsonify({'switch' : switch})

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




# Handle kill signal from OS
def signal_term_handler(signal, frame):
    print 'light switch server killed'
    delete_pid_file()
    sys.exit(0)


signal.signal(signal.SIGTERM, signal_term_handler)


if __name__ == "__main__":
    pid_file = pidfile.PidFile(pid_file_name)

    try:
        app.run(host='0.0.0.0', port=_PORT, debug=DEBUG)
    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
    pid_file.cleanup()
    print 'light switch server shutting down...'
