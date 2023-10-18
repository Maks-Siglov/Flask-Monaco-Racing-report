from app.app import app
from app.bl.report.prepare import prepare
from app.api.utils import json_data_for_report, json_data_for_driver

from werkzeug.exceptions import HTTPException
from flask import request
from flask_restful import Api, Resource, reqparse

api = Api(app)

PREPARED_DATA = prepare()

parser = reqparse.RequestParser()
parser.add_argument('format', type=str, location='args', default='json')
parser.add_argument('order', type=str, location='args', default='asc')


class Report(Resource):
    def get(self):
        args = parser.parse_args()
        if args['order'] == 'desc':
            PREPARED_DATA.reverse()

        if args['format'] == 'json':
            return json_data_for_report(PREPARED_DATA)
        else:
            pass


class Drivers(Resource):
    def get(self):
        args = parser.parse_args()
        if args['order'] == 'desc':
            PREPARED_DATA.reverse()

        if args['format'] == 'json':
            return json_data_for_report(PREPARED_DATA)
        else:
            pass


class UniqueDriver(Resource):
    def get(self, driver_id: str):
        for driver in PREPARED_DATA:
            if driver.abr == driver_id:

                json_data = json_data_for_driver(driver)

                return json_data

        raise HTTPException(response='404')


api.add_resource(Report, '/api/v1/report')
api.add_resource(Drivers, '/api/v1/report/drivers/')
api.add_resource(UniqueDriver, '/api/v1/report/drivers/<string:driver_id>/')


if __name__ == '__main__':
    app.run(debug=True)
