from sqlalchemy import ScalarResult
from flask import make_response, jsonify, Response

from app.db.models.reports import Result, Driver


def json_response_api_report(query_result: ScalarResult) -> Response:
    """This function generate json response for /api/v1/report

    :param query_result: ScalarResult of query through which we can iterate and
    take drivers
    """
    data = {driver.abr: {'name': driver.name, 'team': driver.team}
            for driver in query_result}

    return make_response(jsonify(data))


def json_response_api_drivers(query_result: list[tuple[Result, Driver]]
                              ) -> Response:
    """This function generate json response for /api/v1/report/drivers/"""
    data = {driver.name: _prepare_json_driver(result, driver)
            for result, driver in query_result}

    return make_response(jsonify(data))


def json_response_api_driver(result: Result, driver: Driver) -> Response:
    """This function generate json response for
     /api/v1/report/drivers/<string:driver_id>/
     """
    data = {driver.name: _prepare_json_driver(result, driver)}

    return make_response(jsonify(data))


def _prepare_json_driver(result: Result, driver: Driver) -> dict:
    """This funtion prepare json data for json_response_api_drivers/driver

     :param result: result object which contains data about driver result
     :param driver: driver object which contains data about drivers abr, team,
     name
     :return: dict which contain data about driver
     """
    json_driver = {
            'position': result.position,
            'team': driver.team,
            'lap_time': result.total_seconds
    }
    return json_driver
