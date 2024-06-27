from config import Config
from flask import Flask,render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_restx import Api
from flask.cli import with_appcontext
import click

db = SQLAlchemy()
bootstrap = Bootstrap4()
migrate = Migrate()
admin_manager = Admin(name='flask interview', template_mode='bootstrap4')
login_manager = LoginManager()
api = Api()

import logging

def create_app() ->Flask:
	app = Flask(__name__)
	app.config.from_object(Config())
	configure_logging(app)
	app.config['admin'] = admin_manager
	app = register_apps(app)
	app = register_blueprints(app)
	app = register_api(app)
	app = register_cli_commands(app)
	return app

def register_cli_commands(app):
	@app.cli.command("list_routes")
	def list_routes():
		import urllib
		output = []
		for rule in app.url_map.iter_rules():
			methods = ','.join(rule.methods)
			line = urllib.parse.unquote(f"{rule.endpoint:50s} {methods:20s} {str(rule)}")
			output.append(line)
			for line in sorted(output):
				print(line)

	from app.models import User,AnonymousUser

	@app.cli.command("create-admin")
	@with_appcontext
	def create_admin():
		if User.query.filter_by(username="admin").first():
			click.echo(f"User \"admin\" already exists.")
			return
		
		admin_user = User(username="admin", password="admin", admin=True)
		db.session.add(admin_user)
		db.session.commit()
		click.echo(f"Admin user \"admin\" created")				

	return app

def register_apps(app:Flask) ->Flask:
	bootstrap.init_app(app)
	from app.models import User,AnonymousUser
	db.init_app(app)
	migrate.init_app(app,db=db)
	login_manager.init_app(app)
	login_manager.login_view = 'auth.login'
	admin_manager.init_app(app=app)
	from app.admin import MyUserView
	admin_manager.add_view(MyUserView(User, db.session))

	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(int(user_id))

	login_manager.anonymous_user = AnonymousUser

	return app

def register_blueprints(app:Flask) -> Flask:
	from app.auth import auth_bp
	from app.main import main_bp    
	
	app.register_blueprint(main_bp)
	app.register_blueprint(auth_bp, url_prefix='/auth')

	return app

def register_api(app) ->Flask:
	from app.apis import api_v1,api_v1_bp
	from app.main import nsv1 as main_v1_ns
	from app.auth import nsv1 as auth_v1_ns
	from app.admin import nsv1 as admin_v1_ns
	from app.users import nsv1 as user_v1_ns
	api_v1.add_namespace(main_v1_ns,path="/index")
	api_v1.add_namespace(auth_v1_ns,path="/auth")
	api_v1.add_namespace(admin_v1_ns,path="/admin")
	api_v1.add_namespace(user_v1_ns,path="/users")
	app.register_blueprint(api_v1_bp,url_prefix="/api/v1")
	return app

def configure_logging(app):
    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # Set the desired logging level

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Get the app's logger and attach the console handler
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.DEBUG)