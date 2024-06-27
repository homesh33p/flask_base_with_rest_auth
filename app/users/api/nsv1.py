from flask_restx import Resource,fields
from flask import current_app
from http import HTTPStatus
from . import admin_token_required,token_required,nsv1,all_users_list,base_parser,get_logged_in_user,user_model,me_model,list_users,list_all_users

nsv1.models[me_model.name] = me_model
nsv1.models[user_model.name] = user_model
nsv1.models[all_users_list.name] = all_users_list

@nsv1.route("/me", endpoint="me")
class GetUser(Resource):

    @nsv1.doc(security="Bearer")
    @nsv1.response(int(HTTPStatus.OK), "Token is currently valid.", me_model)
    @nsv1.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @nsv1.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @nsv1.expect(base_parser,validate=True)
    @nsv1.marshal_with(me_model)
    @token_required
    def get(self):
        """Validate access token and return user info for the token bearer."""
        return get_logged_in_user()

@nsv1.route("/all-users")
class Register(Resource):
    @nsv1.doc(security="Bearer")
    @nsv1.doc("list_all_users", description="list all users")
    @nsv1.response(int(HTTPStatus.OK),description="get list of all users(admin and non admin)", model=all_users_list)    
    @nsv1.marshal_with(all_users_list, code=200, description="Successful fetch")
    @nsv1.expect(base_parser,validate=True)
    @admin_token_required
    def get(self):
        """Return all users info."""        
        response = list_all_users()
        return response,HTTPStatus.OK

@nsv1.route("/all-admin", endpoint="admin_list")
class GetAdminUsers(Resource):

    @nsv1.doc(security="Bearer")
    @nsv1.response(int(HTTPStatus.OK),description="get list of all admin users", model=all_users_list) 
    @nsv1.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @nsv1.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @nsv1.response(int(HTTPStatus.FORBIDDEN), "Insufficient Privileges.")    
    @nsv1.expect(base_parser,validate=True)
    @nsv1.marshal_with(all_users_list)
    @admin_token_required
    def get(self):
        """Return all admin users info."""
        response =  list_users(admin=True)
        return response,HTTPStatus.OK    
    
@nsv1.route("/all-non-admin", endpoint="non-admin_list")
class GetNonAdminUsers(Resource):
    """Handles HTTP requests to URL: /api/v1/admin-list."""

    @nsv1.doc(security="Bearer")
    @nsv1.response(int(HTTPStatus.OK), description="get list of all non admin users",model=all_users_list) 
    @nsv1.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @nsv1.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @nsv1.response(int(HTTPStatus.FORBIDDEN), "Insufficient Privileges.")    
    @nsv1.expect(base_parser,validate=True)
    @nsv1.marshal_with(all_users_list)
    @admin_token_required
    def get(self):
        """Return all non admin users info."""
        response = list_users(admin=False)
        return response,HTTPStatus.OK    