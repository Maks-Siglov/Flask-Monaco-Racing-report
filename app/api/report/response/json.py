from flask import make_response, jsonify, Response

from app.db.models.reports import Result, Driver


def json_response_api_report(prepared_data: list[tuple[Result, Driver]]
                             ) -> Response:
    """This function generate json response for /api/v1/report

    :param prepared_data: list with tuples, which contain two object, first -
    result which keeps results of driver, second - driver with it name, abr and
    team
    """
    data = {driver.abr: {'name': driver.name, 'team': driver.team}
            for _, driver in prepared_data}

    return make_response(jsonify(data))


def json_response_api_drivers(prepared_data: list[tuple[Result, Driver]]
                              ) -> Response:
    """This function generate json response for /api/v1/report/drivers/"""
    data = {driver.name: _prepare_json_driver(result, driver)
            for result, driver in prepared_data}

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
