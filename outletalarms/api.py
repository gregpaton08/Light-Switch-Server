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


class OutletAlarm(Resource):
    def get(self, alarm_id):
        print('get for {0}'.format(alarm_id))

    def put(self, alarm_id):
        print('put for {0}'.format(alarm_id))

    def delete(self, alarm_id):
        print('delete for {0}'.format(alarm_id))


class OutletAlarmList(Resource):
    def get(self):
        print('get OutletAlarmList')

    def post(self):
        try:
            data = json.loads(request.data)
        except ValueError:
            print('ERROR: invalid JSON received')
        try:
            print(data)
            scheduler.add_job(test_job_function, 'cron', day_of_week=data['days'], hour=data['hour'], minute=data['minute'])
        except Exception as e:
            return { 'message' : 'ERROR: failed to create alarm {0}'.format(e) }, 400


api.add_resource(OutletAlarmList, '/alarms')
api.add_resource(OutletAlarm, '/alarms/<alarm_id>')
