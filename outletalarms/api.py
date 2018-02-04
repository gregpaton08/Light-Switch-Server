from flask import Flask, render_template, request, jsonify, abort, make_response
from flask_restful import Resource, Api
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import json
from switch_hardware import server


app = Flask(__name__)
api = Api(app)

_API_URL_ROUTE = '/api/v1.0/'

sqlite_db_file_name = 'jobs.sqlite'
jobstores = {
    'default' : SQLAlchemyJobStore(url='sqlite:///' + sqlite_db_file_name)
}
scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()

switch = server.outletswitch.OutletSwitch()

# API JSON Data
# {
#     id : <id>,
#     name : <alarm name>
#     enabled : <true|false>,
#     action : <action>,
#     minute : <minute>,
#     hour : <hour>,
#     days : <days>
# }
#
# example:
# {
#     id : 1,
#     name : 'daily morning alarm'
#     enabled : true,
#     action : 'switch 0 on',
#     minute : 0,
#     hour : 6,
#     days : '0,1,2,3,4,5,6'
# }

def _set_switch_status(status):
    switch.set_status(status)

action_dict = {
    'set_switch_status' : _set_switch_status
}

def _string_to_bool(bool_string):
    if bool_string.lower() in [ 'true', '1', 'yes', 'on']:
        return True
    elif bool_string.lower() in [ 'false', '0', 'no', 'off' ]:
        return False
    else:
        raise Exception('invalid boolean value {0}'.format(bool_string))

def _job_to_dict(job):
    field_value = lambda job, field: [x for x in job.trigger.fields if x.name == field][0].__str__()
    return {
        'id' : job.id,
        'name' : job.name,
        'enabled' : True,
        'action' : job.func.__name__,
        'minute' : field_value(job, 'minute'),
        'hour' : field_value(job, 'hour'),
        'days' : field_value(job, 'day_of_week')
    }

class OutletAlarm(Resource):
    def get(self, alarm_id):
        try:
            job = scheduler.get_job(alarm_id)
            return _job_to_dict(job)
        except:
            return { 'message' : 'ERROR: no alarm found for id {0}'.format(alarm_id) }

    def put(self, alarm_id):
        try:
            data = json.loads(request.data)
        except ValueError:
            return { 'message' : 'ERROR: received invalid JSON' }, 400

        try:
            job = _job_to_dict(scheduler.get_job(alarm_id))
            scheduler.modify_job(alarm_id, name=data.get('name', job['name']))
            scheduler.reschedule_job(job['id'], trigger='cron', day_of_week=data.get('days', job['days']), hour=data.get('hour', job['hour']), minute=data.get('minute', job['minute']))
            return self.get(alarm_id)
        except:
            return { 'message' : 'ERROR: no alarm found for id {0}'.format(alarm_id) }

    def delete(self, alarm_id):
        try:
            scheduler.remove_job(alarm_id)
        except:
            return { 'message' : 'ERROR: no alarm found for id {0}'.format(alarm_id) }


class OutletAlarmList(Resource):
    def get(self):
        jobs = scheduler.get_jobs()
        field_value = lambda job, field: [x for x in job.trigger.fields if x.name == field][0].__str__()
        return [ _job_to_dict(job) for job in jobs], 200

    def post(self):
        try:
            data = json.loads(request.data)
        except ValueError:
            return { 'message' : 'ERROR: received invalid JSON' }, 400

        try:
            # validate the JSON
            for key in [ 'action', 'days', 'hour', 'minute' ]:
                if not data.has_key(key):
                    raise Exception('JSON missing value for key \'{0}\''.format(key))

            action = data['action'].split(' ')
            function_name = action[0]
            arguments = action[1:]
            if not action_dict.has_key(function_name):
                raise Exception('invalid action: {0}'.format(function_name))
            scheduler.add_job(action_dict[function_name], 'cron', day_of_week=data['days'], hour=data['hour'], minute=data['minute'], name=data.get('name', None), args=arguments)
        except Exception as e:
            return { 'message' : 'ERROR: failed to create alarm. {0}'.format(e) }, 400

        return 200


api.add_resource(OutletAlarmList, '/alarms')
api.add_resource(OutletAlarm, '/alarms/<alarm_id>')
