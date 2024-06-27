class Config():
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://flask:flask@localhost:5433/flask"
    LOGS_PATH = "logs"
    SQLALCHEMY_TRACK_MODIFICATIONS = False	
    ADMIN = "admin"	
    TOKEN_EXPIRE_HOURS = 1
    TOKEN_EXPIRE_MINUTES = 0
	
    @staticmethod
    def init_app(app):
        pass	    