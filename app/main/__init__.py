from app import db
from ..models import User,AnonymousUser
from flask import Blueprint
main_bp = Blueprint("main",__name__)
from . import views
from .api import nsv1