from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config, TestingConfig




app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models
from app.routes import auth as auth_blueprint
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    return app


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app

def create_app(config):
    flaskApp = Flask(__name__)
    flaskApp.config.from_object(config)

    db.init_app(flaskApp)

    return flaskApp

from app import create_app,db
from config import Deploymentconfig

flaskApp = create_app(Deploymentconfig)
migrate = Migrate(db,flaskApp)
test_app = create_app(TestingConfig)

