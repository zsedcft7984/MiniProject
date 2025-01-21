from pathlib import Path
from flask_migrate import Migrate
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from apps.config import config
# DB 초기화
db = SQLAlchemy()

# CSRF 보호 초기화
csrf = CSRFProtect()

# 로그인 매니저 초기화
login_manager = LoginManager()

login_manager.login_view = "auth.signup"
login_manager.login_message = ""

def create_app(configKey):
    app = Flask(__name__)

    # 설정 불러오기
    app.config.from_object(config[configKey])

    # DB 초기화
    db.init_app(app)

    # CSRF 보호 활성화
    csrf.init_app(app)

    # 로그인 매니저 초기화
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # 로그인되지 않으면 리디렉션할 URL

    # Blueprints 등록
    from apps.web import views as web_views
    app.register_blueprint(web_views.web, url_prefix='/web')

    from apps.crud import views as crud_views
    app.register_blueprint(crud_views.crud, url_prefix='/crud')

    from apps.auth import views as auth_views
    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    @app.route('/')
    def index():
        return redirect(url_for('web.home'))  # '/web/home'으로 리디렉션

    Migrate(app, db)

    login_manager.init_app(app)

    return app
