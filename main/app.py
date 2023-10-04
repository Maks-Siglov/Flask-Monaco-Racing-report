from flask import Flask, render_template, request, make_response, Response
from main.prepare import prepare

TEMPLATE_FOLDER = r'..\templates'
PREPARED_DATA = prepare()

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)


@app.route('/report')
def common_statistics() -> str:
    """Shows common statistics in web application

    :return: render HTML template
    """
    return render_template('statistics.html', prepared_data=PREPARED_DATA)


@app.route('/report/drivers/')
def drivers_code() -> str:
    """Shows a list of driver's names and codes. Code is a link to info about drivers.

    :return: render HTML template
    """
    order = request.args.get('order', 'asc')

    if order == 'desc':
        PREPARED_DATA.reverse()

    return render_template('drivers_code.html', prepared_data=PREPARED_DATA)


@app.route('/report/drivers/<driver_id>')
def drivers_id(driver_id: int) -> str | Response:
    """Shows info about a driver.

    :param driver_id: id of the driver
    :return: render HTML template
     """
    for index, item in PREPARED_DATA:
        if driver_id == item[3]:
            return render_template('driver_id.html',
                                   prepared_data=PREPARED_DATA, driver_id=driver_id)

    return make_response(render_template('404.html'), 404)


@app.errorhandler(404)
def not_found(error) -> Response:
    return make_response(render_template('404.html'), 404)


if __name__ == '__main__':
    app.run(debug=True)
