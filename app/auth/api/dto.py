from flask_restx import reqparse
import re

def validate_username(value:str)->str:
    if len(value) > 15:
        raise ValueError('Username must be 15 characters or less')
    return value

def validate_password(value:str)->str:
    if len(value) < 5:
        raise ValueError('Password must be at least 5 characters long')
    if not re.search(r'[A-Za-z]', value):
        raise ValueError('Password must contain at least one alphabet')
    if not re.search(r'[0-9]', value):
        raise ValueError('Password must contain at least one number')
    if not re.search(r'[\W_]', value):  # \W matches any non-alphanumeric character, including special characters
        raise ValueError('Password must contain at least one special character')
    return value

reg_parser = reqparse.RequestParser()
reg_parser.add_argument('username', type=validate_username, location="json",required=True, nullable=False)
reg_parser.add_argument('password', type=validate_password, location="json",required=True, nullable=False)

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, location="json",required=True, nullable=False)
login_parser.add_argument('password', type=str, location="json",required=True, nullable=False)

renew_parser = reqparse.RequestParser()
renew_parser.add_argument('Authorization', type=str, location='headers', required=True, help='Bearer token required')