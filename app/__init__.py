from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from elasticsearch import Elasticsearch

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'main.login'
migrate = Migrate()
mail = Mail()

def page_not_found(e):
    return render_template('/layout/page_not_found.html', company="EcoHUB"), 404

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None
    from app.blueprint import main
    app.register_blueprint(main)

    app.register_error_handler(404, page_not_found)

    return app

from app import models