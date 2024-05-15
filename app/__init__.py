from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'main.login'
migrate = Migrate()

def page_not_found(e):
    return render_template('/layout/page_not_found.html', company="EcoHUB"), 404

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.blueprint import main
    app.register_blueprint(main)

    app.register_error_handler(404, page_not_found)

    return app

from app import models
# Flaskapp = create_app(Config)
# migrate = Migrate(db, Flaskapp)


# app = Flask(__name__)
# app.config.from_object(Config)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# login = LoginManager(app)
# login.login_view = 'login'


# db = SQLAlchemy()
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'

# def create_app():
#     app = Flask(__name__)
#     from app.blueprint import main
#     app.register_blueprint(main)
    
#     return app

# def create_app(config_class=Config):
#     app = Flask(__name__)
#     app.config.from_object(config_class)

#     db.init_app(app)
#     login_manager.init_app(app)
    
#     from app.blueprint import main
#     app.register_blueprint(main, url_prefix='/main')
#     return app

# flaskApp = create_app(ProductionConfig)
# migrate = Migrate(db, flaskApp)

# if __name__ == "__main__":
#     flaskApp.run()


# from app import routes, models
# from app.routes import auth as auth_blueprint