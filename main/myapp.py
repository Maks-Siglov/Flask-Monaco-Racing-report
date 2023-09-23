from main.report import build_report
from main.utils import read_log_files
from flask import Flask, render_template, request

DATA_FOLDER_PATH = './data'
TEMPLATE_FOLDER = r'..\templates'

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)


def prepare() -> list:
    """This function prepare data for web application

    :return: data which used for creating web application
    """
    start_log, end_log, abbreviations_data = read_log_files(DATA_FOLDER_PATH)
    prepared_data = build_report(start_log, end_log, abbreviations_data)
    prepared_data.sort(key=lambda x: x[2])
    prepared_data = list(enumerate(prepared_data, start=1))

    return prepared_data


@app.route('/report')
def common_statistics():
    """Shows common statistics in web application

    :return: render HTML template
    """
    prepared_data = prepare()

    return render_template('statistics.html', prepared_data=prepared_data)


@app.route('/report/drivers/')
def drivers_code():
    """Shows a list of driver's names and codes. Code is a link to info about drivers.

    :return: render HTML template
    """
    prepared_data = prepare()
    order = request.args.get('order', 'asc')

    if order == 'desc':
        prepared_data.reverse()

    return render_template('drivers_code.html', prepared_data=prepared_data)


@app.route('/report/drivers/<driver_id>')
def drivers_id(driver_id):
    """Shows info about a driver.

    :return: render HTML template
     """
    prepared_data = prepare()

    return render_template('driver_id.html', prepared_data=prepared_data, driver_id=driver_id)


if __name__ == '__main__':
    app.run(debug=True)
