from flask import (Blueprint, render_template, request, make_response,
                   Response, g)

report_bp = Blueprint('report', __name__)
error_bp = Blueprint('errors', __name__)


@report_bp.route('/', methods=['GET'])
@report_bp.route('/report/', methods=['GET'])
def report() -> str:
    """Shows common statistics in web application

    :return: render HTML template
    """
    order = request.args.get('order')

    if order == 'desc':
        g.PREPARED_DATA.reverse()

    return render_template('report.html', prepared_data=g.PREPARED_DATA)


@report_bp.route('/report/drivers/', methods=['GET'])
def drivers() -> str:
    """Shows a list of driver's names and codes.
     Code is a link to info about drivers.

    :return: render HTML template
    """
    order = request.args.get('order')

    if order == 'desc':
        g.PREPARED_DATA.reverse()

    return render_template('drivers.html', prepared_data=g.PREPARED_DATA)


@report_bp.route('/report/drivers/<string:driver_id>', methods=['GET'])
def unique_driver(driver_id) -> str | Response:
    """Shows a statistics about unique driver

    :param driver_id: driver abbreviation
    :return: render HTML template or Response if driver not exist in report
    """

    if not any(driver_id == driver.abr for driver, _ in g.PREPARED_DATA):
        return make_response(render_template('404.html'), 404)

    return render_template('unique_driver.html',
                           prepared_data=g.PREPARED_DATA, driver_id=driver_id)


@error_bp.app_errorhandler(404)
def not_found(error) -> Response:
    """andle a 404 Not Found error

    :param error: the 404 error
    :return a 404 error response, which contains custom error HTML page
    """
    return make_response(render_template('404.html'), 404)
