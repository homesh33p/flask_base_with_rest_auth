from .. import User,Result,login,register,refresh_token,ApiForbidden,ApiUnauthorized
from flask_restx import Namespace

nsv1 = Namespace(name="auth_v1",
                       description="version 1 of the API of authentication  functionality")

from .nsv1 import *