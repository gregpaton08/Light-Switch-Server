#!/usr/bin/env python

from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time
import thread
import os
from crontab import CronTab
import signal
import sys
import lsauth
app = Flask(__name__)

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
		cron = CronTab()
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
		job = cron.new(command='/home/pi/projects/light_switch/light_on.sh')
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
	cron = CronTab()
	iter = cron.find_comment(comment)
	try:
		job = iter.next()
		while len(job) > 0:
			cron.remove(job)
			job = iter.next()
	except StopIteration:
		pass
	cron.write()

def createCronComment(minute, hour, days):
	comment = 'ls_server_'
        comment += str(minute)
        comment += '_'
        comment += str(hour)
        comment += '_'
        comment += str(days)
	return comment

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
		app.run(host='0.0.0.0', port=3333, debug=DEBUG)
	except KeyboardInterrupt:
		deletePidFile()
	deletePidFile()
	print 'light switch server shutting down...'
