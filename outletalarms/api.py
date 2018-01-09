from flask import Flask, render_template, request, jsonify, abort, make_response
from flask_restful import Resource, Api
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


app = Flask(__name__)
api = Api(app)

_API_URL_ROUTE = '/api/v1.0/'

sqlite_db_file_name = 'jobs.sqlite'
jobstores = {
    'default' : SQLAlchemyJobStore(url='sqlite:///' + sqlite_db_file_name)
}
scheduler = BackgroundScheduler(jobstores=jobstores)

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
        print('post OutletAlarmList')


api.add_resource(OutletAlarmList, '/alarms')
api.add_resource(OutletAlarm, '/alarms/<alarm_id>')