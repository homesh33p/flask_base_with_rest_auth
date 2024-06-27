from flask_restx import Namespace

nsv1 = Namespace(name="main_v1",description="version 1 of the API of main functionality")
from .nsv1 import *