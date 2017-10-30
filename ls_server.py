#!/usr/bin/env python

from flask import Flask, render_template, request, jsonify, abort, make_response
import RPi.GPIO as GPIO
import time
import thread
import os
from crontab import CronTab
import signal
import sys
import lsauth
import lsswitches
import ls

app = Flask(__name__)

_PORT = 3333
DEBUG = True
pidFileName = 'ls_server_pid'
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



# Toggles a GPIO channel from low to high
def toggle_gpio_channel(channel, seconds = 2):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.OUT)
    GPIO.output(channel, GPIO.HIGH)
    time.sleep(seconds)
    GPIO.output(channel, GPIO.LOW)
    GPIO.cleanup(channel)


def set_light_status(on):
    channel = ls.GPIO_LIGHT_OFF
    if on:
        channel = ls.GPIO_LIGHT_ON
    thread.start_new_thread(toggle_gpio_channel, (channel,) )


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
            set_light_status(request.json['status'])
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
    set_light_status(switch['status'])

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
    set_light_status(True)
    return render_template('main.html')


@app.route("/light_off")
@lsauth.requires_auth
def light_off():
    set_light_status(False)
    return render_template('main.html')


@app.route("/light_auth")
@lsauth.requires_auth
def light_auth():
    return render_template('main.html')


@app.route("/alarms", methods=['POST'])
def post_alarms():
    if not request.json:
        return jsonify({'error' : 'no json found'}), 400

    alarm = {
        'user'   : request.json.get('user', None),
        'action' : request.json.get('action', None),
        'minute' : request.json.get('minute', None),
        'hour'   : request.json.get('hour', None),
        'dow'    : request.json.get('dow', None),
    }

    for key, value in alarm.iteritems():
        if value is None:
            return jsonify({'error' : 'JSON is missing entry for ' + key}), 400

    # find the next available alarm id
    alarms = get_alarms_list()
    id = 0
    sorted_alarms = sorted(alarms, key=lambda k: k['id']) 
    print(sorted_alarms)
    for curr in sorted_alarms:
        if id == curr['id']:
            id = id + 1
        else:
            break;
    alarm['id'] = id

    ret, error = create_alarm(alarm['user'], alarm['action'], alarm['minute'], alarm['hour'], alarm['dow'], id)
    if ret:
        return jsonify({ 'alarms' : alarm }), 201
    
    return jsonify({'error' : 'unable to set alarm: ' + error}), 400


@app.route("/alarms", methods=['GET'])
def get_alarms():
    alarms = get_alarms_list()

    return jsonify({ 'alarms' : alarms }), 201


@app.route("/alarms", methods=['DELETE'])
def delete_alarms():
    if not request.json:
        return jsonify({'error' : 'no json found'}), 400
    
    id = request.json.get('id', None)
    if not id:
        return jsonify({'error' : 'invalid json'}), 400 

    alarms = get_alarms_list()
    print(alarms)
    alarm = [x for x in alarms if int(x['id']) == int(id)]
    if len(alarm) != 1:
        error_string = 'unable to find an alarm for id ' + str(id)
        return jsonify({'error' : error_string}), 400

    alarm = alarm[0]

    if delete_alarm(id):
        return jsonify({ 'alarms' : alarm }), 201
    else:
        return jsonify({'error' : 'unable to delete alarm'}), 400


# action: 'on' to create an alarm that turns device on or 'off' to turn device off it.
# minute: 0 tp 59
# hour: 0 to 23
# days: 0 is Sunday, 6 is Saturday. Comma separated list for multiple days.
# id is the unique identifier of the alarm (used in the comment).
def create_alarm(user, action, minute, hour, days, id):
    comment = create_cron_comment(user, action, minute, hour, days, id)
    # If alarm already exists return True
    cron = CronTab(user=True)
    iter = cron.find_comment(comment)
    try:
        job = iter.next()
        if len(job) > 0:
            if DEBUG:
                print job
            return True, 'alarm already exists'
    except StopIteration:
        pass
    # print comment
    if action == 'on':
        job = cron.new(command='/home/pi/projects/light_switch/light_on.py')
    elif action == 'off':
        job = cron.new(command='/home/pi/projects/light_switch/light_off.py')
    else:
        return False, 'Invalid action ' + action
    job.set_comment(comment)
    job.minute.on(minute)
    job.hour.on(hour)
    daysList = days.split(",")
    job.dow.on(*daysList)
    if DEBUG:
        print job
    if job.is_valid():
        cron.write()
        return True, 'success'
    else:
        return False, 'Invalid cron job ' + str(job)


def delete_alarm(id):
    cron = CronTab(user=True)
    ret = False
    for job in cron:
        comment = job.comment
        if 'ls_server' in comment:
            comment = comment[comment.find('id=') + 3:]
            if int(id) == int(comment):
                cron.remove(job)
                ret = True
            
    cron.write()

    return ret


def create_cron_comment(user, action, minute, hour, days, id):
    comment = 'ls_server'
    comment += '_user='   + user
    comment += '_action=' + action
    comment += '_minute=' + str(minute)
    comment += '_hour='   + str(hour)
    comment += '_days='   + str(days)
    comment += '_id='     + str(id)
    return comment


def get_alarms_list():
    alarms = []
    cron = CronTab(user=True)
    for job in cron:
        if 'ls_server' in job.comment:
            job_info = {}
            job_info['minute'] = str(job.minute)
            job_info['hour'] = str(job.hour)
            job_info['dow'] = str(job.dow)
            if 'id=' in job.comment:
                id = job.comment
                id = id[id.find("id=") + 3:]
                job_info['id'] = int(id)
            else:
                job_info['id'] = -1
            alarms.append(job_info)

    return alarms


def createPidFile():
	pidFile = open(pidFileName, 'w')
	pidFile.write(str(os.getpid()))
	pidFile.close()


def delete_pid_file():
    try:
        os.remove(pidFileName)
    except OSError:
        pass


# Handle kill signal from OS
def signal_term_handler(signal, frame):
    print 'light switch server killed'
    delete_pid_file()
    sys.exit(0)


signal.signal(signal.SIGTERM, signal_term_handler)


if __name__ == "__main__":
	try:
		createPidFile()
		app.run(host='0.0.0.0', port=_PORT, debug=DEBUG)
	except KeyboardInterrupt:
		pass
	delete_pid_file ()
	print 'light switch server shutting down...'
