from flask import Blueprint, render_template, request, make_response, Response
from app.bl.prepare import prepare

PREPARED_DATA = prepare()

router = Blueprint('router', __name__)
error = Blueprint('errors', __name__)


@router.route('/', methods=['GET'])
@router.route('/report/', methods=['GET'])
def report() -> str:
    """Shows common statistics in web application

    :return: render HTML template
    """
    order = request.args.get('order')

    if order == 'desc':
        PREPARED_DATA.reverse()

    return render_template('report.html', prepared_data=PREPARED_DATA)


@router.route('/report/drivers/', methods=['GET'])
def drivers() -> str | Response:
    """Shows a list of driver's names and codes.
     Code is a link to info about drivers.

    :return: render HTML template
    """
    order = request.args.get('order')
    driver_id = request.args.get('driver_id')

    if order == 'desc':
        PREPARED_DATA.reverse()

    if driver_id and not any(
            driver_id == driver.abr for driver in PREPARED_DATA):
        return make_response(render_template('404.html'), 404)

    return render_template('drivers.html', prepared_data=PREPARED_DATA,
                           driver_id=driver_id)


@error.errorhandler(404)
def not_found(error) -> Response:
    """andle a 404 Not Found error

    :param error: the 404 error
    :return a 404 error response, which contains custom error HTML page
    """
    return make_response(render_template('404.html'), 404)
