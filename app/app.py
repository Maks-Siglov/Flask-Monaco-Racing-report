from flask import Flask
from flasgger import Swagger
from flask_restful import Api

from app.api.report.routers import Report, Drivers, UniqueDriver, cache
from app.site.routers import report_bp, error_bp
from app.bl.report.prepare import prepare_db
from app.db.session import check_db


check_db()
prepare_db()

TEMPLATE_FOLDER = 'site/templates'

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
api = Api(app)
swagger = Swagger(app)
cache.init_app(app)

app.register_blueprint(report_bp)
app.register_blueprint(error_bp)

api.add_resource(Report, '/api/v1/report/')
api.add_resource(Drivers, '/api/v1/report/drivers/')
api.add_resource(UniqueDriver, '/api/v1/report/drivers/<string:driver_id>/')


if __name__ == '__main__':
    app.run(debug=True)
