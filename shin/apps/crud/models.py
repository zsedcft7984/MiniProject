from datetime import datetime

from apps.app import db, login_manager       #  flaskbook/apps/app.py 으로부터 db를 import합니다.
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# db.Model을 상속한 User 클래스를 작성한다 모델정의하기
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True)
    email = db.Column(db.String(100), unique=True, index=True)
    password_hash = db.Column(db.String(255))  # 길이를 255로 설정

    carts = db.relationship('Cart', back_populates='user', lazy=True)

    @property
    def password(self):
        raise ArithmeticError("읽어 들일 수 없음")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_duplicate_email(self):
        return User.query.filter_by(email=self.email).first() is not None

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



