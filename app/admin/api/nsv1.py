from flask_restx import Resource,fields
from flask import current_app
from http import HTTPStatus
from . import admin_token_required,register_admin,delete_user,nsv1
from .dto import reg_parser,base_parser

token_response_model = nsv1.model('RegisterResponse', {
    'status': fields.String(description='Status of the registration'),
    'message': fields.String(description='Registration message'),
    'access_token': fields.String(description='JWT access token'),
    'token_type': fields.String(description='Type of the token'),
    'expires_in': fields.Integer(description='Token expiration time in seconds'),
})

@nsv1.route("/register")
class Register(Resource):
    @nsv1.doc(security="Bearer")
    @nsv1.doc("register_admin_user", description="Register an admin user with a username and password")
    @nsv1.marshal_with(token_response_model, code=201, description="Successful registration")
    @nsv1.expect(reg_parser,validate=True)
    @admin_token_required
    def post(self):
        args = reg_parser.parse_args()
        username = args['username']
        password = args['password']
        response = register_admin(username,password)
        return response,HTTPStatus.CREATED,{"Cache-Control":"no-store","Pragma":"no-cache"}

base_response_model = nsv1.model('BaseResponse', {
    'status': fields.String(description='Status of the operation'),
    'message': fields.String(description='message')
})

@nsv1.route("/delete/<int:user_id>")
class Deregister(Resource):
    @nsv1.doc(security="Bearer")
    @nsv1.doc("delete_user", description="Delete a user")
    @nsv1.marshal_with(base_response_model, code=200, description="Successful deletion")
    @nsv1.expect(base_parser,validate=True)
    @admin_token_required
    def delete(self,user_id):
        response = delete_user(user_id)
        return response,HTTPStatus.OK

 
