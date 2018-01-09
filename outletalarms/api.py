from flask import Flask, render_template, request, jsonify, abort, make_response
from flask_restful import Resource, Api
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
api = Api(app)

_API_URL_ROUTE = '/api/v1.0/'

sqlite_db_file_name = 'jobs.sqlite'
jobstores = {
    'default' : SQLAlchemyJobStore(url='sqlite:///' + sqlite_db_file_name)
}
scheduler = BackgroundScheduler(jobstores=jobstores)

class OutletAlarmAPI(Resource):
    def get(self, alarm_id):
        print('get for {0}'.format(alarm_id))

    def put(self, alarm_id):
        print('put for {0}'.format(alarm_id))

api.add_resource(OutletAlarmAPI, _API_URL_ROUTE + 'alarm/<string:alarm_id>')