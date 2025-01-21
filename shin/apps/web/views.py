from apps.app import db
from apps.web.models import Cart, CartItem, Menu
from flask import Blueprint, render_template, redirect, url_for, request
from apps.web.models import Menu
from flask_login import current_user

web = Blueprint(
    "web",
    __name__,
    template_folder="templates",
    static_folder="static"
)

@web.route('/')
def index():
    return redirect(url_for('web.home'))

@web.route('/home')
def home():
    breadcrumb = [
        {'name': 'HOME', 'url': None}  # 현재 페이지는 활성 상태로 표시
    ]
    return render_template('web/home.html', breadcrumb=breadcrumb)

@web.route('/menu')
def menu():
    # Menu 테이블에서 모든 메뉴 항목을 가져오기
    burgers = Menu.query.filter_by(category='버거').all()  # '버거' 카테고리의 모든 항목 가져오기
    sides = Menu.query.filter_by(category='사이드').all()  # '사이드' 카테고리의 모든 항목 가져오기
    drinks = Menu.query.filter_by(category='음료').all()  # '음료' 카테고리의 모든 항목 가져오기
    
    breadcrumb = [
        {'name': 'HOME', 'url': url_for('web.home')},  # 'HOME'은 홈페이지로 링크
        {'name': '메뉴', 'url': None}  # 현재 페이지는 URL 없이 표시
    ]
    
    return render_template('web/menu.html', breadcrumb=breadcrumb, burgers=burgers, sides=sides, drinks=drinks)

@web.route('/events')
def events():
    breadcrumb = [
        {'name': 'HOME', 'url': url_for('web.home')},  # 'HOME'은 홈페이지로 링크
        {'name': '이벤트', 'url': None}  # 현재 페이지는 URL 없이 표시
    ]
    return render_template('web/events.html', breadcrumb=breadcrumb)

@web.route('/order')

def order():
    breadcrumb = [
        {'name': 'HOME', 'url': url_for('web.home')},  
        {'name': '주문하기', 'url': None}  
    ]


    return render_template('web/order.html', breadcrumb=breadcrumb)

@web.route('/add_to_cart/<menu_name>', methods=['POST'])
def add_to_cart(menu_name):
    menu_item = Menu.query.filter_by(name=menu_name).first()
    if menu_item:
        # 로그인한 사용자의 장바구니 확인
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)
            db.session.commit()
        
        # 장바구니에 동일한 항목이 있는지 확인
        cart_item = CartItem.query.filter_by(cart_id=cart.id, menu_name=menu_item.name).first()
        if cart_item:
            cart_item.quantity += 1  # 수량 증가
        else:
            cart_item = CartItem(menu_name=menu_item.name, quantity=1, cart=cart)
            db.session.add(cart_item)

        db.session.commit()

    return redirect(url_for('web.menu'))