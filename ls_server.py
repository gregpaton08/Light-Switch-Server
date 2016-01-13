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
app = Flask(__name__)

_PORT = 3333
DEBUG = True
CHANNEL_ON = 17
CHANNEL_OFF = 23
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


def turn_light_on(turnOn):
    channel = CHANNEL_OFF
    if turnOn:
        channel = CHANNEL_ON
    thread.start_new_thread(setChannelHigh, (channel,) )

@app.route(_URL_ROUTE, methods=['POST'])
def add_switch():
    if not request.json:
        return jsonify({'error', 'no json found'}), 400
    
    switch = {
        'room'   : request.json.get('room',   u''),
        'device' : request.json.get('device', u''),
        'status' : request.json.get('status', False),
    }
    lsswitches.add_switch(switch)    

    return jsonify({'switch': switch}), 201

@app.route(_URL_ROUTE + '/<int:switch_id>', methods=['DELETE'])
def delete_switch(switch_id):
    lsswitches.delete_switch(switch_id)
    return jsonify({'result': True})

@app.route(_URL_ROUTE, methods=['GET'])
def route():
    switches = lsswitches.get_switches()
    return jsonify({'switches' : switches})

@app.route(_URL_ROUTE + '/<int:switch_id>', methods=['PUT'])
def update_switch(switch_id):
    switches = lsswitches.get_switches()
    switch = [switch for switch in switches if switch['id'] == switch_id]
    if 0 == len(switch):
        abort(400)
    if not request.json:
        print('NO JSON ==================')
        abort(400)
    if 'status' in request.json:
        pass
        if type(request.json['status']) is not bool:
            abort(400)
        else:
            turn_light_on(request.json['status'])
    switch[0]['status'] = request.json.get('status', switch[0]['status'])
    
    return jsonify({'switch': switch[0]})

@app.route("/")
@lsauth.requires_auth
def light_main():
	return render_template('main.html')

@app.route("/light_on")
@lsauth.requires_auth
def light_on():
    thread.start_new_thread(setChannelHigh, (CHANNEL_ON,) )
    return render_template('main.html')
	
@app.route("/light_off")
@lsauth.requires_auth
def light_off():
    thread.start_new_thread(setChannelHigh, (CHANNEL_OFF,) )
    return render_template('main.html')

@app.route("/light_auth")
@lsauth.requires_auth
def light_auth():
    return render_template('main.html')

@app.route("/set_alarm", methods=['GET', 'POST'])
def set_alarm():
    state = request.args.get('state', '')
    minute = request.args.get('minute', '')
    hour   = request.args.get('hour', '')
    days   = request.args.get('days', '')
    if setAlarm(state, minute, hour, days):
        dayNums = days.split(",")
        dayList = []
        for i in dayNums:
            dayList.append(DAYS_OF_WEEK[int(i)])
        print dayList
        templateData = {
            'minute' : minute,
            'hour' : str(int(hour) % 12),
            'AMPM' : 'PM' if int(hour) > 12 else 'AM',
            'days' : dayList
        }
        return render_template('alarm_set.html', **templateData)
    else:
        return render_template('alarm_fail.html')

@app.route("/alarms", methods=['POST'])
def post_alarms():
    if not request.json:
        return jsonify({'error' : 'no json found'}), 400

    alarm = {
        'minute' : request.json.get('minute',   u''),
        'hour'   : request.json.get('hour', u''),
        'dow'    : request.json.get('dow', u''),
    }

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

    if setAlarm('on', alarm['minute'], alarm['hour'], alarm['dow']):
        return jsonify({ 'alarms' : alarm }), 201
    else:
        return jsonify({'error' : 'unable to set alarm'}), 400

@app.route("/alarms", methods=['GET'])
def get_alarms():
    alarms = get_alarms_list()

    return jsonify({ 'alarms' : alarms }), 201

@app.route("/alarms", methods=['DELETE'])
def delete_alarms():
    if not request.json:
        return jsonify({'error' : 'no json found'}), 400

    alarm = {
        'minute' : request.json.get('minute',   u''),
        'hour'   : request.json.get('hour', u''),
        'dow'    : request.json.get('dow', u''),
    }

    if deleteAlarm(alarm['minute'], alarm['hour'], alarm['dow']):
        return jsonify({ 'alarms' : alarm }), 201
    else:
        return jsonify({'error' : 'unable to delete alarm'}), 400

@app.route("/delete_alarm", methods=['GET', 'POST'])
def delete_alarm():
    minute = request.args.get('minute', '')
    hour   = request.args.get('hour', '')
    days   = request.args.get('days', '')
    deleteAlarm(minute, hour, days)
    dayNums = days.split(",")
    dayList = []
    for i in dayNums:
        dayList.append(DAYS_OF_WEEK[int(i)])
        templateData = {
                'minute' : minute,
                'hour' : str(int(hour) % 12),
                'AMPM' : 'PM' if int(hour) > 12 else 'AM',
                'days' : dayList
        }
        return render_template('alarm_delete.html', **templateData)

def setChannelHigh(channel):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.OUT)
    GPIO.output(channel, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(channel, GPIO.LOW)
    GPIO.cleanup(channel)

# state: 'on' to create an alarm or 'off' to delete it.
# minute: 0 tp 59
# hour: 0 to 23
# days: 0 is Sunday, 6 is Saturday. Comma separated list for multiple days.
def setAlarm(state, minute, hour, days):
	if state == 'on':
		comment = createCronComment(minute, hour, days)
		# If alarm already exists return True
		cron = CronTab(user=True)
		iter = cron.find_comment(comment)
		try:
			job = iter.next()
			if len(job) > 0:
				if DEBUG:
					print job
				return True
		except StopIteration:
			pass
		#print comment
		job = cron.new(command='/home/pi/projects/light_switch/light_on.py')
		job.set_comment(comment)
		job.minute.on(minute)
		job.hour.on(hour)
		daysList = days.split(",")
		job.dow.on(*daysList)
		if DEBUG:
			print job
		if job.is_valid():
			cron.write()
			return True
		else:
			return False
	elif state == 'off':
		pass
	else:
		# Error handling
		return False

def deleteAlarm(minute, hour, days):
    comment = createCronComment(minute, hour, days)
    print(comment)
    cron = CronTab(user=True)
    ret = False
    for job in cron.find_comment(comment):
        cron.remove(job)
        ret = True
            
    cron.write()

    return ret

def createCronComment(minute, hour, days):
    comment = 'ls_server_'
    comment += str(minute)
    comment += '_'
    comment += str(hour)
    comment += '_'
    comment += str(days)
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

def deletePidFile():
	try:
                os.remove(pidFileName)
        except OSError:
                pass

# Handle kill signal from OS
def signal_term_handler(signal, frame):
	print 'light switch server killed'
	deletePidFile()
	sys.exit(0)

signal.signal(signal.SIGTERM, signal_term_handler)


if __name__ == "__main__":
	try:
		createPidFile()
		app.run(host='0.0.0.0', port=_PORT, debug=DEBUG)
	except KeyboardInterrupt:
		deletePidFile()
	deletePidFile()
	print 'light switch server shutting down...'
