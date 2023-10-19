from flask import Flask
from app.site.routes import report_bp
from app.site.routes import error_bp
from flasgger import Swagger

TEMPLATE_FOLDER = 'site/templates'

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
swagger = Swagger(app)

app.register_blueprint(report_bp)
app.register_blueprint(error_bp)


if __name__ == '__main__':
    app.run(debug=True)
