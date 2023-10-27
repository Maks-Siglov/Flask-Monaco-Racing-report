from flask import make_response, jsonify, Response

from app.db.models.reports import Result


def json_response_api_report(prepared_data: list[Result]) -> Response:
    """This function generate json response for /api/v1/report

    :param prepared_data: list with result object which also contain data about
    driver and his results
    """
    data = {result.driver.abr: {
        'name': result.driver.name, 'team': result.driver.team
    }
            for result in prepared_data}

    return make_response(jsonify(data))


def json_response_api_drivers(prepared_data: list[Result]) -> Response:
    """This function generate json response for /api/v1/report/drivers/"""
    data = {result.driver.name: _prepare_json_driver(result)
            for result in prepared_data}

    return make_response(jsonify(data))


def json_response_api_driver(result: Result) -> Response:
    """This function generate json response for
     /api/v1/report/drivers/<string:driver_id>/
     """
    data = {result.driver.name: _prepare_json_driver(result)}

    return make_response(jsonify(data))


def _prepare_json_driver(result: Result) -> dict:
    """This funtion prepare json data for json_response_api_drivers/driver

     :param result: result object which contains data about driver and his
      results
     :return: dict which contain data about driver
     """
    json_driver = {
            'position': result.position,
            'team': result.driver.team,
            'lap_time': result.total_seconds
    }
    return json_driver
