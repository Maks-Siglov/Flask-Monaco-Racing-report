from flask import make_response, jsonify, Response

from app.db.models.reports import Driver, Result


def json_response_api_report(prepared_data: list[tuple[Driver, Result]]
                             ) -> Response:
    """This function generate json response for /api/v1/report

    :param prepared_data: list with tuples which contains two object, first -
    driver with it name, abr and team, second - result with driver results in
    race (position, time)
    """
    data = {driver.abr: {'name': driver.name, 'team': driver.team}
            for driver, _ in prepared_data}

    return make_response(jsonify(data))


def json_response_api_drivers(prepared_data: list[tuple[Driver, Result]]
                              ) -> Response:
    """This function generate json response for /api/v1/report/drivers/"""
    data = {driver.name: _prepare_json_driver(driver, result)
            for driver, result in prepared_data}

    return make_response(jsonify(data))


def json_response_api_driver(driver: Driver, result: Result) -> Response:
    """This function generate json response for
     /api/v1/report/drivers/<string:driver_id>/
     """
    data = {driver.name: _prepare_json_driver(driver, result)}

    return make_response(jsonify(data))


def _prepare_json_driver(driver: Driver, result: Result) -> dict:
    """This funtion prepare json data for single
     for json_response_api_drivers/driver

     :param driver: driver object, that contains name, abr, team
     :param result: result object which belong to driver, contains driver
      position, and time results in race
     :return: dict which contain data about driver
     """
    json_driver = {
            'position': result.position,
            'team': driver.team,
            'lap_time': result.total_seconds
    }
    return json_driver
