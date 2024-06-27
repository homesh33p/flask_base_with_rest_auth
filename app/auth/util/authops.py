from flask import jsonify,current_app
from http import HTTPStatus
from flask_restx import abort
from . import db,User,token_required,decoded_exp_time_to_str

def register(username,password)->dict:
    if db.session.query(User).filter(User.username==username).first():
        abort(HTTPStatus.CONFLICT, f"{username} is already registered", status="fail")
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    access_token = new_user.encode_access_token()
    response = dict(
        status="success",
        message="successfully registered",
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

def login(username,password)->dict:
    user = db.session.query(User).filter(User.username==username).first()
    if (not user) or (not user.check_password(password=password)):
        abort(HTTPStatus.FORBIDDEN, f"Incorrect username/password", status="fail")     
    access_token = user.encode_access_token()
    response = dict(
        status="success",
        message="successfully logged in",
            # This step is necessary because JSON does not support binary data (bytes) directly, and everything needs to be encoded as strings.

            # However, as of Python 3.6+, the encode() and decode() methods are typically not necessary when working with strings and bytes in this context, as JWT libraries usually return the token as a string. Thus, you might not need to explicitly decode the token unless your encode_access_token method is returning bytes.
        access_token=access_token,
        token_type="bearer",
        expires_in=_get_token_expire_time(),
        admin=user.admin
    )
    return response

def refresh_token(existing_token)->dict:
    result = User.decode_access_token(access_token=existing_token)
    if not result.success:
        abort(code=HTTPStatus.NOT_ACCEPTABLE,message=result.error)
    # invalidate the token/blacklist it, to be implemented
    
    #create the user obj
    user = db.session.query(User).filter(User.id==result.value['public_id']).first()
    response = dict(
        status="success",
        message="successfully renewed token",
            # This step is necessary because JSON does not support binary data (bytes) directly, and everything needs to be encoded as strings.

            # However, as of Python 3.6+, the encode() and decode() methods are typically not necessary when working with strings and bytes in this context, as JWT libraries usually return the token as a string. Thus, you might not need to explicitly decode the token unless your encode_access_token method is returning bytes.
        access_token=user.encode_access_token(),
        token_type="bearer",
        expires_in=_get_token_expire_time(),
        admin=user.admin
    )
    return response
