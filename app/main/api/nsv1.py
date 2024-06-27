from flask_restx import Resource
from . import nsv1

@nsv1.route("/<string:username>")
class Index(Resource):
    def get(self,username):
        return {"msg":f"Hi {username}"}