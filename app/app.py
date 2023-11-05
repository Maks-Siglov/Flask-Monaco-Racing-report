from flask import Flask
from flasgger import Swagger
from flask_restful import Api
from typing import Any

from app.api.report.routers import Report, Drivers, UniqueDriver, cache
from app.db.session import set_session, pop_session, close_dbs
from app.site.routers import report_bp, error_bp
from app.bl.report.prepare import prepare_db
from app.config import APP_PORT, APP_HOST, APP_DEBUG

TEMPLATE_FOLDER = 'site/templates'


def create_app() -> Flask:

    app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
    api = Api(app)
    swagger = Swagger(app)
    cache.init_app(app)

    prepare_db()

    app.before_request(set_session)

    @app.teardown_request
    def handle_session(args) -> Any:
        pop_session()
        return args

    @app.teardown_appcontext
    def close_db(args) -> Any:
        close_dbs()
        return args

    app.register_blueprint(report_bp)
    app.register_blueprint(error_bp)

    api.add_resource(Report, '/api/v1/report/')
    api.add_resource(Drivers, '/api/v1/report/drivers/')
    api.add_resource(UniqueDriver, '/api/v1/report/drivers/<string:driver_id>/')

    return app


if __name__ == '__main__':
    create_app().run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)