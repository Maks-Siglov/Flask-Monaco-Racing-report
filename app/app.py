from flask import Flask
from flasgger import Swagger
from flask_restful import Api

from app.api.report import Report, Drivers, UniqueDriver
from app.site.routes import report_bp
from app.site.routes import error_bp

TEMPLATE_FOLDER = 'site/templates'

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
api = Api(app)
swagger = Swagger(app)

app.register_blueprint(report_bp)
app.register_blueprint(error_bp)

api.add_resource(Report, '/api/v1/report/')
api.add_resource(Drivers, '/api/v1/report/drivers/')
api.add_resource(UniqueDriver, '/api/v1/report/drivers/<string:driver_id>/')


if __name__ == '__main__':
    app.run(debug=True)
