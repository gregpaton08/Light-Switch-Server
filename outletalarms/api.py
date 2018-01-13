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
        'enabled' : True,
        'action' : job.func.__name__,
        'minute' : field_value(job, 'minute'),
        'hour' : field_value(job, 'hour'),
        'days' : field_value(job, 'day_of_week')
    }

class OutletAlarm(Resource):
    def get(self, alarm_id):
        print('get for {0}'.format(alarm_id))
        try:
            job = scheduler.get_job(alarm_id)
        except:
            return { 'message' : 'ERROR: no alarm found for id {0}'.format(alarm_id) }

    def put(self, alarm_id):
        print('put for {0}'.format(alarm_id))

    def delete(self, alarm_id):
        print('delete for {0}'.format(alarm_id))


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
            print(data)
            scheduler.add_job(test_job_function, 'cron', day_of_week=data['days'], hour=data['hour'], minute=data['minute'])
        except Exception as e:
            return { 'message' : 'ERROR: failed to create alarm {0}'.format(e) }, 400

        return 200


api.add_resource(OutletAlarmList, '/alarms')
api.add_resource(OutletAlarm, '/alarms/<alarm_id>')
