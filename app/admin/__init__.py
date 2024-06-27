from app import db
from ..models import User
from ..util import Result
from ..auth import admin_token_required,ApiForbidden,ApiUnauthorized
from .util import register_admin,delete_user,ApiNotFound

from .views import MyUserView
from .api import nsv1