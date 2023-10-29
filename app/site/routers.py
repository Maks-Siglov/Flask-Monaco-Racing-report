from flask import Blueprint, render_template, request, make_response, Response
from sqlalchemy import select

from app.db.models.reports import Result, Driver
from app.db.session import get_session


report_bp = Blueprint('report', __name__)
error_bp = Blueprint('errors', __name__)


@report_bp.route('/', methods=['GET'])
@report_bp.route('/report/', methods=['GET'])
def report() -> str:
    """Shows common statistics in web application

    :return: render HTML template
    """
    with get_session() as session:
        order = request.args.get('order')
        statement = select(Driver)

        if order == 'desc':
            statement = select(Driver).order_by(Driver.abr.desc())

        result = session.scalars(statement)
        print(result)
        return render_template('report.html', query_result=result)


@report_bp.route('/report/drivers/', methods=['GET'])
def drivers() -> str:
    """Shows a list of driver's names and codes.
     Code is a link to info about drivers.

    :return: render HTML template
    """
    with get_session() as session:
        order = request.args.get('order')
        statement = select(Result, Driver).join(Driver).order_by(
            Result.position)

        if order == 'desc':
            statement = select(Result, Driver).join(Result).order_by(
                Result.position.desc())

        result = session.execute(statement).all()

        return render_template('drivers.html', query_result=result)


@report_bp.route('/report/drivers/<string:driver_id>', methods=['GET'])
def unique_driver(driver_id) -> str | Response:
    """Shows a statistics about unique driver

    :param driver_id: driver abbreviation
    :return: render HTML template or Response if driver not exist in report
    """

    with get_session() as session:
        statement = select(Result, Driver).join(Driver).where(
            Driver.abr == driver_id)
        item = session.execute(statement).one_or_none()
        if not item:
            return make_response(render_template('404.html'), 404)

        result, driver = item

    return render_template('unique_driver.html', result=result, driver=driver)


@error_bp.app_errorhandler(404)
def not_found(error) -> Response:
    """andle a 404 Not Found error

    :param error: the 404 error
    :return a 404 error response, which contains custom error HTML page
    """
    return make_response(render_template('404.html'), 404)
