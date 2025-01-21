from apps.app import db
from apps.crud.models import User

# Cart 모델: 사용자와 카트를 연결
class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 관계 설정: User와 Cart의 관계를 설정
    user = db.relationship('User', back_populates='carts')
    items = db.relationship('CartItem', back_populates='cart', lazy=True)

# Menu 모델: 메뉴 항목 정의
class Menu(db.Model):
    __tablename__ = "menu"
    name = db.Column(db.String(100), primary_key=True)  # name을 기본 키로 설정
    quantity = db.Column(db.Integer, nullable=False)  # 메뉴의 기본 수량
    category = db.Column(db.String(50), nullable=False)  # 메뉴 카테고리

    # CartItem과의 관계 설정
    cart_items = db.relationship('CartItem', back_populates='menu', lazy=True)

# CartItem 모델: 카트에 담긴 메뉴 항목
class CartItem(db.Model):
    __tablename__ = "cart_item" 
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    menu_name = db.Column(db.String(100), db.ForeignKey('menu.name'), nullable=False)  # Menu의 name과 연결
    quantity = db.Column(db.Integer, nullable=False, default=1)  # CartItem에 있는 메뉴의 수량
    
    # Cart와의 관계 설정
    cart = db.relationship('Cart', back_populates='items')
    
    # Menu와의 관계 설정
    menu = db.relationship('Menu', back_populates='cart_items')
