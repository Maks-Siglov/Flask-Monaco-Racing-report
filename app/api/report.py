from app.app import app
from flask_restful import Api, Resource

api = Api(app)


class Report(Resource):
    pass
