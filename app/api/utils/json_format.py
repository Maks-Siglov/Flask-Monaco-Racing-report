from app.bl.report.models import Driver
from flask import make_response, jsonify, Response


def json_response_api_report(prepared_data: list[Driver]) -> Response:
    """This function generate json response for /api/v1/report"""
    data = {driver.abr: {'name': driver.name, 'team': driver.team}
            for driver in prepared_data}

    return make_response(jsonify(data))


def json_response_api_drivers(prepared_data: list[Driver]) -> Response:
    """This function generate json response for /api/v1/report/drivers/"""
    data = {driver.name: _prepare_json_driver(driver)
            for driver in prepared_data}

    return make_response(jsonify(data))


def json_response_api_driver(driver: Driver) -> Response:
    """This function generate json response for
     /api/v1/report/drivers/<string:driver_id>/
     """
    data = {driver.name: _prepare_json_driver(driver)}

    return make_response(jsonify(data))


def _prepare_json_driver(driver: Driver) -> dict:
    """This funtion prepare json data for single
     for json_response_api_drivers/driver

     :param: driver about whom we are prepared data
     :return: dict which contain data about driver
     """
    json_driver = {
            'position': driver.position,
            'team': driver.team,
            'lap_time': driver.lap_time.total_seconds
    }
    return json_driver
