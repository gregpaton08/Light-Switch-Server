
from flask import Flask, render_template, request, jsonify, abort, make_response
from flask_restful import Resource, Api
import json
from switch_hardware import server


DEBUG = False
pid_file_name = 'ls_server_pid'


app = Flask(__name__)
api = Api(app)


_API_URL_ROUTE = '/api/v1.0/'

switch = server.outletswitch.OutletSwitch()

class LightSwitchAPI(Resource):
    def __init__(self):
        print('init LightSwitchAPI')
        self.switch = switch

    def get(self):
        try:
            return { 'status' : self.switch.get_status() }
        except:
            return { 'message' : 'ERROR: failed to get switch status' }, 400

    def put(self):
        if not request.is_json:
            return { 'message' : 'Data provided must be in JSON format.' }, 400

        data = json.loads(request.data)
        try:
            self.switch.set_status(data['status'])
        except:
            return { 'message' : 'ERROR: failed to set switch status' }, 400

        return { 'status' : data['status'] }

api.add_resource(LightSwitchAPI, _API_URL_ROUTE + 'light_status')


@app.route("/")
def light_main():
    return render_template('main.html')
