from app.bl.report.models import Driver
from flask import make_response, jsonify, Response


def json_response_api_report(prepared_data: list[Driver]) -> Response:
    data = {driver.abr: {'name': driver.name, 'team': driver.team}
            for driver in prepared_data}

    return make_response(jsonify(data))


def json_response_api_drivers(prepared_data: list[Driver]) -> Response:
    data = {driver.name: _prepare_json_driver(driver)
            for driver in prepared_data}

    return make_response(jsonify(data))


def json_response_api_driver(driver: Driver) -> Response:
    data = {driver.name: _prepare_json_driver(driver)}

    return make_response(jsonify(data))


def _prepare_json_driver(driver: Driver) -> dict:

    json_driver = {
            'position': driver.position,
            'team': driver.team,
            'lap_time': driver.lap_time.total_seconds
    }
    return json_driver
