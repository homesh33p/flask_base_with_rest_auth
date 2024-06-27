from flask_restx import Namespace
from .. import db,User,Result,ApiForbidden,ApiUnauthorized,admin_token_required,register_admin,delete_user,ApiNotFound

nsv1 = Namespace('admin_V1', description='Version 1  of admin operations')    
from .nsv1 import *