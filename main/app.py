from flask import Flask
from main.report_routes import router as report_routes
from main.report_routes import error as error_routes

TEMPLATE_FOLDER = r'..\templates'

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)

app.register_blueprint(report_routes)
app.register_blueprint(error_routes)


if __name__ == '__main__':
    app.run(debug=True)
