from flask import Flask
import flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app import create_app,db
from config import DeploymentConfig
db = SQLAlchemy()
def create_app(config):
    flaskApp = flask(__name__)
    flaskApp.config.from_object(config)
    
    db.init_app(flaskApp)

    return flaskApp

Flaskapp = create_app(DeploymentConfig)
migrate = Migrate(db, Flaskapp)


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
#initialize only at the end#
#why do we want to migrate the database? we should work on the currrent database in memory?every single time we run the test it will create a new database#
 


