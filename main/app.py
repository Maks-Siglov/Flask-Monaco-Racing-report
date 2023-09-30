from main.utils import utils_for_app
from flask import Flask, render_template, request, abort
from cli import start_parser

TEMPLATE_FOLDER = r'..\templates'
PREPARED_DATA = utils_for_app.prepare()

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
def drivers_id(driver_id: int) -> str:
    """Shows info about a driver.

    :param driver_id: id of the driver
    :return: render HTML template
     """
    for index, item in PREPARED_DATA:
        if driver_id == item[3]:
            return render_template('driver_id.html', prepared_data=PREPARED_DATA, driver_id=driver_id)
    abort(404)


if __name__ == '__main__':
    ARGS_FILES, ARGS_DRIVER, ARGS_DESC = start_parser()
    app.run(debug=True)
