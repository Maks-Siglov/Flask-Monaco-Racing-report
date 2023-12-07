import atexit

from typing import Any

from flask import Flask
from flasgger import Swagger
from flask_restful import Api

from app.config import (
    APP_HOST,
    APP_PORT,
    APP_DEBUG,
    TEMPLATE_FOLDER,
)
from app.db.session import (
    close_dbs,
    pop_session,
    set_session,
)
from app.site.routers import (
    error_bp,
    report_bp,
)
from app.api.report.routers import (
    Report,
    Drivers,
    UniqueDriver,
    cache,
)

API_REPORT_ROUTE = '/api/v1/report'
API_DRIVERS_ROUTE = '/api/v1/report/drivers'


def create_app() -> Flask:
    app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
    api = Api(app)
    Swagger(app)
    cache.init_app(app)

    app.before_request(set_session)

    @app.teardown_request
    def handle_session(args: Any) -> Any:
        pop_session()
        return args

    app.register_blueprint(report_bp)
    app.register_blueprint(error_bp)

    api.add_resource(Report, API_REPORT_ROUTE)
    api.add_resource(Drivers, API_DRIVERS_ROUTE)
    api.add_resource(UniqueDriver, f'{API_DRIVERS_ROUTE}/<string:driver_id>')

    return app


app = create_app()

if __name__ == '__main__':
    atexit.register(close_dbs)
    assert APP_PORT
    app.run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
