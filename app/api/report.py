from app.app import app
from app.bl.report.prepare import prepare
from app.api.utils.json_format import (
    json_response_for_report,
    json_response_for_drivers,
    json_response_for_driver
)
from app.api.utils.xml_format import (
    xml_response_for_report,
    xml_response_for_drivers,
    xml_response_for_driver
)
from flask import make_response, render_template, Response
from flask_restful import Api, Resource, reqparse

api = Api(app)

PREPARED_DATA = prepare()

parser = reqparse.RequestParser()
parser.add_argument('format', type=str, location='args', default='json')
parser.add_argument('order', type=str, location='args', default='asc')


class Report(Resource):
    def get(self) -> Response:
        args = parser.parse_args()
        if args['order'] == 'desc':
            PREPARED_DATA.reverse()

        if args['format'] == 'xml':
            return xml_response_for_report(PREPARED_DATA)

        return json_response_for_report(PREPARED_DATA)


class Drivers(Resource):
    def get(self) -> Response:
        args = parser.parse_args()
        if args['order'] == 'desc':
            PREPARED_DATA.reverse()

        if args['format'] == 'xml':
            return xml_response_for_drivers(PREPARED_DATA)

        return json_response_for_drivers(PREPARED_DATA)


class UniqueDriver(Resource):
    def get(self, driver_id: str) -> Response:
        args = parser.parse_args()
        for driver in PREPARED_DATA:
            if driver.abr == driver_id:

                if args['format'] == 'xml':
                    return xml_response_for_driver(driver)

                return json_response_for_driver(driver)

        return make_response(render_template('404.html'), 404)


api.add_resource(Report, '/api/v1/report')
api.add_resource(Drivers, '/api/v1/report/drivers/')
api.add_resource(UniqueDriver, '/api/v1/report/drivers/<string:driver_id>/')


if __name__ == '__main__':
    app.run(debug=True)
