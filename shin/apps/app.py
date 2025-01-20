from pathlib import Path
from flask_migrate import Migrate
from flask import Flask, redirect, url_for
from apps.config import config
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db=SQLAlchemy()

csrf = CSRFProtect()

def create_app(configKey) :
    app = Flask(__name__)

    app.config.from_object(config[configKey])

    db.init_app(app)


    from apps.web import views as web_views
    app.register_blueprint(web_views.web, url_prefix='/web')


    @app.route('/')
    def index():
        return redirect(url_for('web.home'))  # '/web/home'으로 리디렉션
    
    Migrate(app, db)

    return app