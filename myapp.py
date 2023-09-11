from main.report import Report
from main.utils import ReaderFiles
from flask import Flask, render_template

app = Flask(__name__)


def prepare():
    start_log, end_log, abbreviations_data = ReaderFiles(r'./data').read_log_files()
    prepared_data = Report(start_log, end_log, abbreviations_data).build_report()
    prepared_data.sort(key=lambda x: x[2])
    prepared_data = list(enumerate(prepared_data, start=1))

    return prepared_data


@app.route('/report')
def common_statistics():
    prepared_data = prepare()

    return render_template('statistics.html', prepared_data=prepared_data)


@app.route('/report/drivers')
def drivers_code():
    prepared_data = prepare()

    return render_template('drivers_code.html', prepared_data=prepared_data)


if __name__ == '__main__':
    app.run(debug=True)
