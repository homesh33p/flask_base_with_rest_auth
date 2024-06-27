from flask_login import UserMixin,AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime,timedelta,UTC
from flask import current_app
from . import db,Result

class User(UserMixin,db.Model):
    __tablename__="user"

    def __init__(self,**kwargs) -> None:
        super(User, self).__init__(**kwargs)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    admin = db.Column(db.Boolean, default=False,nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @property
    def is_admin(self):
        return self.admin
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    def get_id(self):
        return str(self.id)
    
    def encode_access_token(self):
        now = datetime.now(UTC)
        token_age_h = current_app.config.get("TOKEN_EXPIRE_HOURS")
        token_age_m = current_app.config.get("TOKEN_EXPIRE_MINUTES")
        expire = now + timedelta(hours=token_age_h, minutes=token_age_m)
        if current_app.config["TESTING"]:
            expire = now + timedelta(seconds=5)
        payload = dict(exp=expire, iat=now, sub=self.id,admin=self.admin)
        key = current_app.config.get("SECRET_KEY")
        return jwt.encode(payload, key, algorithm="HS256")
    
    @staticmethod
    def decode_access_token(access_token):
        if isinstance(access_token, bytes):
            access_token = access_token.decode("ascii")
        if access_token.startswith("Bearer "):
            split = access_token.split("Bearer")
            access_token = split[1].strip()
        try:
            key = current_app.config.get("SECRET_KEY")
            payload = jwt.decode(access_token, key, algorithms=["HS256"])
            return Result.Ok(dict(payload))
        except jwt.ExpiredSignatureError:
            error = "Authorization token expired. Please log in again."
            return Result.Fail(error)
        except jwt.InvalidTokenError:
            error = "Invalid token. Please log in again."
            return Result.Fail(error)
    
class AnonymousUser(AnonymousUserMixin):
    pass