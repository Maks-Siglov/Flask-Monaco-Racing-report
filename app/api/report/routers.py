

from flask import (
    Response,
    make_response,
    render_template,
)
from flask_caching import Cache
from flask_restful import (
    Resource,
    reqparse,
)

from app.crud.report import (
    report_query,
    drivers_query,
    unique_driver_query,
)
from app.api.report.response.xml import (
    xml_response_api_driver,
    xml_response_api_report,
    xml_response_api_drivers,
)
from app.api.report.response.json import (
    json_response_api_driver,
    json_response_api_report,
    json_response_api_drivers,
)

parser = reqparse.RequestParser()
parser.add_argument('format', type=str, location='args', default='json')
parser.add_argument('order', type=str, location='args', default='asc')

cache = Cache(config={'CACHE_TYPE': 'flask_caching.backends.SimpleCache'})


class Report(Resource):
    def get(self) -> Response:
        """
        This is the documentation for the /api/v1/report endpoint.

        GET:
        This operation retrieves a report.
        ---
        parameters:
          - name: format
            in: query
            type: string
            enum: ['json', 'xml']
            default: 'json'
          - name: order
            in: query
            type: string
            enum: ['asc', 'desc']
            default: 'asc'

        responses:
          200:
            description: Returns a report in the specified format.
            schema:
              type: object
              properties:
                data:
                  type: string
        """
        args = parser.parse_args()
        _format = args.get('format', 'json')
        order = args.get('order', 'asc')

        cache_key = f"report_{order}_{_format}"
        if cache_response := cache.get(cache_key):
            return cache_response

        result = report_query(order)

        if _format == 'xml':
            response = xml_response_api_report(result)
        else:
            response = json_response_api_report(result)

        cache.set(cache_key, response, timeout=3600)

        return response


class Drivers(Resource):
    def get(self) -> Response:
        """
        This is the documentation for the /api/v1/drivers endpoint.

        GET:
        This operation retrieves statistics about drivers.
        ---
        parameters:
          - name: format
            in: query
            type: string
            enum: ['json', 'xml']
            default: 'json'
          - name: order
            in: query
            type: string
            enum: ['asc', 'desc']
            default: 'asc'

        responses:
          200:
            descriptions: Returns statistics about drivers
            schema:
              type: object
              properties:
                data:
                  type: string
        """
        args = parser.parse_args()
        _format = args.get('format', 'json')
        order = args.get('order', 'asc')

        cache_key = f"drivers_{order}_{_format}"
        if cache_response := cache.get(cache_key):
            return cache_response

        result = drivers_query(order)

        if _format == 'xml':
            response = xml_response_api_drivers(result)
        else:
            response = json_response_api_drivers(result)

        cache.set(cache_key, response, timeout=3600)

        return response


class UniqueDriver(Resource):
    def get(self, driver_id: str) -> Response:
        """
        This is the documentation for /api/v1/report/drivers/<string:driver_id>
         endpoint

         GET:
         This operation retrieves a statistic of driver by provided driver_id
         ---
         parameters:
           - name: driver_id
             in: path
             type: string
             required: True
             description: The unique identifier of the driver
           - name: format
             in: query
             type: string
             enum: ['json', 'xml']
             default: 'json'

         responses:
           200:
             descriptions: Return statistic of unique driver
             schema:
               type: object
               properties:
                 data:
                   type: string

           404:
             descriptions: Driver not found, return an error page
        """
        args = parser.parse_args()
        _format = args.get('format', 'json')

        cache_key = f"driver_{driver_id}_{_format}"
        if cache_response := cache.get(cache_key):
            return cache_response

        item = unique_driver_query(driver_id)

        if item is None:
            return make_response(render_template('404.html'), 404)

        result, driver = item
        if _format == 'xml':
            response = xml_response_api_driver(result, driver)
        else:
            response = json_response_api_driver(result, driver)

        cache.set(cache_key, response, timeout=3600)
        return response
