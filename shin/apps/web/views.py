from apps.app import db
from apps.web.models import Cart, CartItem, Menu
from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from apps.web.models import Menu
from flask_login import current_user, login_required

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
    burgers = Menu.query.filter_by(category='burger').all()  # '버거' 카테고리의 모든 항목 가져오기
    sides = Menu.query.filter_by(category='side').all()  # '사이드' 카테고리의 모든 항목 가져오기
    drinks = Menu.query.filter_by(category='drink').all()  # '음료' 카테고리의 모든 항목 가져오기
    
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
    
    # 카테고리별 메뉴 항목 가져오기
    burgers = Menu.query.filter_by(category='burger').all()  # '버거' 카테고리의 모든 항목 가져오기
    sides = Menu.query.filter_by(category='side').all()  # '사이드' 카테고리의 모든 항목 가져오기
    drinks = Menu.query.filter_by(category='drink').all()  # '음료' 카테고리의 모든 항목 가져오기  

    # 로그인된 사용자라면 장바구니의 아이템 수량 계산
    cart_count = 0
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            cart_count = sum(item.quantity for item in cart.items)

    # 로그인되지 않았다면 로그인 페이지로 리다이렉트
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login', next=request.url))
    
    # 주문 페이지 렌더링
    return render_template('web/order.html', breadcrumb=breadcrumb, burgers=burgers, sides=sides, drinks=drinks, cart_count=cart_count)


@web.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    data = request.json  # 클라이언트에서 보낸 JSON 데이터 수신
    menu_name = data.get('menu_name')
    quantity = int(data.get('quantity', 1))

    menu_item = Menu.query.filter_by(name=menu_name).first()
    if not menu_item:
        return jsonify({'success': False, 'message': '메뉴를 찾을 수 없습니다'}), 404

    # 현재 로그인한 사용자의 장바구니 찾기 또는 생성
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()

    # 장바구니에 동일한 항목이 있는지 확인
    cart_item = CartItem.query.filter_by(cart_id=cart.id, menu_name=menu_name).first()
    if cart_item:
        cart_item.quantity += quantity  # 기존 항목 수량 증가
    else:
        cart_item = CartItem(cart_id=cart.id, menu_name=menu_name, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()

    # 장바구니에 담긴 총 수량 반환
    total_items = sum(item.quantity for item in cart.items)
    return jsonify({'success': True, 'cart_count': total_items})

@web.route('/my_cart')
def my_cart():
    # 로그인된 사용자가 있다면 장바구니 정보 가져오기
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            # 장바구니에 담긴 아이템들을 가져오기
            cart_items = cart.items
            total_price = sum(item.quantity * item.menu.quantity for item in cart_items)  # 총 가격 계산
        else:
            cart_items = []
            total_price = 0
    else:
        # 로그인되지 않은 사용자는 장바구니 페이지에 접근할 수 없도록 리다이렉트
        return redirect(url_for('auth.login'))

    return render_template('web/cart.html', cart_items=cart_items, total_price=total_price)


@web.route('/get_cart_count')
def get_cart_count():
    if current_user.is_authenticated:
        # 로그인된 사용자의 장바구니를 가져오기
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            cart_count = sum(item.quantity for item in cart.items)  # 장바구니에 있는 아이템들의 수량 합산
        else:
            cart_count = 0  # 장바구니가 비었으면 0
    else:
        cart_count = 0  # 로그인되지 않았으면 0
    return jsonify({'cart_count': cart_count})  # JSON 형태로 장바구니 개수 반환

@web.route('/preview')
def preview():
    return render_template('web/preview.html')