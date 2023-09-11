import main.cli
from main.report import Report
from main.utils import ReaderFiles
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/report')
def common_statistics():
    start_log, end_log, abbreviations_data = ReaderFiles(r'./data').read_log_files()
    prepared_data = Report(start_log, end_log, abbreviations_data).build_report()
    prepared_data.sort(key=lambda x: x[2])
    prepared_data = list(enumerate(prepared_data, start=1))

    return render_template('statistics.html', prepared_data=prepared_data)


if __name__ == '__main__':
    app.run(debug=True)
