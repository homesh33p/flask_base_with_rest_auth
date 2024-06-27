from functools import wraps
from flask import request
from . import ApiForbidden,ApiUnauthorized,User,Result

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        result = _check_access_token(admin_only=False)
        token_payload = result.value
        for name, val in token_payload.items():
            setattr(decorated, name, val)
        return f(*args, **kwargs)
    
    return decorated

def admin_token_required(f):
    """Execute function if request contains valid access token AND user is admin."""

    @wraps(f)
    def decorated(*args, **kwargs):
        result = _check_access_token(admin_only=True)
        token_payload = result.value
        if not token_payload["admin"]:
            raise ApiForbidden()
        for name, val in token_payload.items():
            setattr(decorated, name, val)
        return f(*args, **kwargs)

    return decorated

def _check_access_token(admin_only):
    token = request.headers.get("Authorization")
    if not token:
        raise ApiUnauthorized(description="Unauthorized",admin_only=admin_only)
    result = User.decode_access_token(token)
    if not result.success:
        raise ApiUnauthorized(
            description=result.error,
            admin_only=admin_only,
            error="invalid_token",
            error_description=result.error,
        )
    return result
        