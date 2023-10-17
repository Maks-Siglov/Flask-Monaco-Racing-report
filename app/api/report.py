from app.app import app
from app.bl.report.prepare import prepare
from app.api.utils import json_data_for_report, json_data_for_driver

from werkzeug.exceptions import HTTPException
from flask import request
from flask_restful import Api, Resource

api = Api(app)

PREPARED_DATA = prepare()


class Report(Resource):
    def get(self):
        order = request.args.get('order')
        if order == 'desc':
            PREPARED_DATA.reverse()

        json_data = json_data_for_report(PREPARED_DATA)

        return json_data


class Drivers(Resource):
    def get(self):
        order = request.args.get('order')
        if order == 'desc':
            PREPARED_DATA.reverse()

        json_data = json_data_for_report(PREPARED_DATA)

        return json_data


class UniqueDriver(Resource):
    def get(self, driver_id: str):
        for driver in PREPARED_DATA:
            if driver.abr == driver_id:

                json_data = json_data_for_driver(driver)

                return json_data

        raise HTTPException(response='404')


api.add_resource(Report, '/api/report/')
api.add_resource(Drivers, '/api/report/drivers/')
api.add_resource(UniqueDriver, '/api/report/drivers/<string:driver_id>/')


if __name__ == '__main__':
    app.run(debug=True)
