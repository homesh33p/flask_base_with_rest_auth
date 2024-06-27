from flask import Blueprint
from flask_restx import Api

blueprint = Blueprint("api_v1",__name__)

api = Api(blueprint,title="API V1",description="Version 1 of the flask interview API",doc='/api-docs')

