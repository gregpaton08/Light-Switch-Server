from flask import Flask, render_template, request, jsonify, abort, make_response
from flask_restful import Resource, Api
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import json


app = Flask(__name__)
api = Api(app)

_API_URL_ROUTE = '/api/v1.0/'

sqlite_db_file_name = 'jobs.sqlite'
jobstores = {
    'default' : SQLAlchemyJobStore(url='sqlite:///' + sqlite_db_file_name)
}
scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()

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


def test_job_function():
    print('test job function')

def job_to_dict(job):
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
            return job_to_dict(job)
        except:
            return { 'message' : 'ERROR: no alarm found for id {0}'.format(alarm_id) }

    def put(self, alarm_id):
        try:
            data = json.loads(request.data)
        except ValueError:
            return { 'message' : 'ERROR: received invalid JSON' }, 400

        try:
            job = job_to_dict(scheduler.get_job(alarm_id))
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
        list_of_json_jobs = []
        for job in jobs:
            list_of_json_jobs.append(job_to_dict(job))

        return list_of_json_jobs, 200

    def post(self):
        try:
            data = json.loads(request.data)
        except ValueError:
            return { 'message' : 'ERROR: received invalid JSON' }, 400
        try:
            scheduler.add_job(test_job_function, 'cron', day_of_week=data['days'], hour=data['hour'], minute=data['minute'], name=data.get('name', None))
        except Exception as e:
            return { 'message' : 'ERROR: failed to create alarm {0}'.format(e) }, 400

        return 200


api.add_resource(OutletAlarmList, '/alarms')
api.add_resource(OutletAlarm, '/alarms/<alarm_id>')
