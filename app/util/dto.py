from flask_restx import reqparse
import re

base_parser = reqparse.RequestParser()
base_parser.add_argument('Authorization', type=str, location='headers', required=True, help='Bearer token required')