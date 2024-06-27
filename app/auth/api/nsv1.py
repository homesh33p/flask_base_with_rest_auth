from flask_restx import Resource,fields
from flask import current_app
from http import HTTPStatus
from . import register,login,refresh_token,nsv1
from .dto import reg_parser,renew_parser,login_parser

token_response_model = nsv1.model('RegisterResponse', {
    'status': fields.String(description='Status of the registration'),
    'message': fields.String(description='Registration message'),
    'access_token': fields.String(description='JWT access token'),
    'token_type': fields.String(description='Type of the token'),
    'expires_in': fields.Integer(description='Token expiration time in seconds'),
})

@nsv1.route("/register")
class Register(Resource):
    @nsv1.doc("register_user", description="Register a new user with a username and password")
    @nsv1.marshal_with(token_response_model, code=201, description="Successful registration")
    @nsv1.expect(reg_parser,validate=True)
    def post(self):
        args = reg_parser.parse_args()
        username = args['username']
        password = args['password']
        response = register(username,password)
        return response,HTTPStatus.CREATED,{"Cache-Control":"no-store","Pragma":"no-cache"}
    
@nsv1.route("/login")
class Login(Resource):
    @nsv1.doc("login_user", description="Log a user in with a username and password and provide access token")
    @nsv1.marshal_with(token_response_model, code=201, description="Successful Login")
    @nsv1.expect(login_parser,validate=True)
    def post(self):
        args = login_parser.parse_args()
        username = args['username']
        password = args['password']
        response = login(username,password)
        return response,HTTPStatus.OK,{"Cache-Control":"no-store","Pragma":"no-cache"}

@nsv1.route("/renew")
class Renew(Resource):
    @nsv1.doc(security="Bearer")
    @nsv1.doc("refresh_token", description="Invalidate the current token and  provide renewed access token")
    @nsv1.marshal_with(token_response_model, code=200, description="Successful renewal")
    @nsv1.expect(renew_parser,validate=True)
    def post(self):
        # Parse the token from the request headers
        args = renew_parser.parse_args()
        existing_token = args['Authorization']
        response = refresh_token(existing_token=existing_token)
        return response,HTTPStatus.OK,{"Cache-Control":"no-store","Pragma":"no-cache"} 



