from flask import jsonify,current_app
from http import HTTPStatus
from flask_restx import abort
from datetime import datetime,UTC
from . import db,User,ApiNotFound

def register_admin(username,password)->dict:
    if db.session.query(User).filter(User.username==username).first():
        abort(HTTPStatus.CONFLICT, f"{username} is already registered", status="fail")
    new_user = User(username=username, password=password,admin=True)
    db.session.add(new_user)
    db.session.commit()
    access_token = new_user.encode_access_token()
    response = dict(
        status="success",
        message="successfully registered admin",
            # This step is necessary because JSON does not support binary data (bytes) directly, and everything needs to be encoded as strings.

            # However, as of Python 3.6+, the encode() and decode() methods are typically not necessary when working with strings and bytes in this context, as JWT libraries usually return the token as a string. Thus, you might not need to explicitly decode the token unless your encode_access_token method is returning bytes.
        access_token=access_token,
        token_type="bearer",
        expires_in=_get_token_expire_time(),
        admin=new_user.admin
    )
    return response

def _get_token_expire_time():
    token_age_h = current_app.config.get("TOKEN_EXPIRE_HOURS")
    token_age_m = current_app.config.get("TOKEN_EXPIRE_MINUTES")
    expires_in_seconds = token_age_h * 3600 + token_age_m * 60
    return expires_in_seconds if not current_app.config["TESTING"] else 5

def delete_user(user_id):
    """
    Delete a user by their user_id.

    Args:
        user_id (int): The ID of the user to delete.

    Returns:
        bool: True if the user was successfully deleted, False otherwise.
    """
    user = User.query.get(user_id)
    
    if not user:
        raise ApiNotFound(user_id=user_id)
    username = user.username    
    db.session.delete(user)
    db.session.commit()
    return dict(
    status="success",
    message=f"successfully deleted user: {username} with id: {user_id}")
