from apps.app import db
from apps.web.models import Cart, CartItem, Menu
from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user, login_required

web = Blueprint(
    "web",
    __name__,
    template_folder="templates",
    static_folder="static"
)
# 홈페이지로 리디렉션
@web.route('/')
def index():
    return redirect(url_for('web.home'))

# 홈 페이지 렌더링
@web.route('/home')
def home():
    breadcrumb = [{'name': 'HOME', 'url': None}]
    return render_template('web/home.html', breadcrumb=breadcrumb)

# 메뉴 페이지 렌더링: '버거', '사이드', '음료' 카테고리의 메뉴 항목을 각각 가져옴
@web.route('/menu')
def menu():
    burgers = Menu.query.filter_by(category='burger').all()
    sides = Menu.query.filter_by(category='side').all()
    drinks = Menu.query.filter_by(category='drink').all()
    breadcrumb = [
        {'name': 'HOME', 'url': url_for('web.home')},
        {'name': '메뉴', 'url': None}
    ]
    return render_template('web/menu.html', breadcrumb=breadcrumb, burgers=burgers, sides=sides, drinks=drinks)

# 이벤트 페이지 렌더링
@web.route('/events')
def events():
    breadcrumb = [
        {'name': 'HOME', 'url': url_for('web.home')},
        {'name': '이벤트', 'url': None}
    ]
    return render_template('web/events.html', breadcrumb=breadcrumb)

# 주문 페이지 렌더링: '버거', '사이드', '음료' 카테고리의 메뉴 항목을 가져오고,
# 로그인된 사용자라면 장바구니 아이템 수량을 계산하여 표시
@web.route('/order')
def order():
    breadcrumb = [
        {'name': 'HOME', 'url': url_for('web.home')},
        {'name': '주문하기', 'url': None}
    ]
    burgers = Menu.query.filter_by(category='burger').all()
    sides = Menu.query.filter_by(category='side').all()
    drinks = Menu.query.filter_by(category='drink').all()
    
    cart_count = 0
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            cart_count = sum(item.quantity for item in cart.items)

    if not current_user.is_authenticated:
        # 로그인되지 않은 사용자는 로그인 페이지로 리디렉션
        return redirect(url_for('auth.login', next=request.url))
    
    return render_template('web/order.html', breadcrumb=breadcrumb, burgers=burgers, sides=sides, drinks=drinks, cart_count=cart_count)


# 장바구니에 메뉴 항목을 추가하는 API:
# 메뉴 항목이 장바구니에 이미 있는지 확인하고, 있으면 수량을 증가시키고,
# 없으면 새로 추가한다.
@web.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    data = request.json
    menu_name = data.get('menu_name')
    quantity = int(data.get('quantity', 1))
    item_type = data.get('item_type', '단품')

    menu_item = Menu.query.filter_by(name=menu_name).first()
    if not menu_item:
        return jsonify({'success': False, 'message': '메뉴를 찾을 수 없습니다'}), 404

    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()

    cart_item = CartItem.query.filter_by(cart_id=cart.id, menu_name=menu_name, is_set=(True if item_type == "세트" else False)).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            menu_name=menu_name,
            quantity=quantity,
            is_set=True if item_type == "세트" else False
        )
        db.session.add(cart_item)

    db.session.commit()

    total_items = sum(item.quantity for item in cart.items)
    return jsonify({'success': True, 'cart_count': total_items})

# 사용자의 장바구니 아이템과 총 가격을 보여주는 페이지
@web.route('/my_cart')
@login_required
def my_cart():
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            cart_items = cart.items
            total_price = 0
            for item in cart_items:
                item_price = item.quantity * item.menu.quantity
                if item.is_set:
                    item_price += 3500 * item.quantity
                total_price += item_price
        else:
            cart_items = []
            total_price = 0
    else:
        return redirect(url_for('auth.login'))

    return render_template('web/cart.html', cart_items=cart_items, total_price=total_price)

# 로그인된 사용자의 장바구니 아이템 수량을 반환하는 API
@web.route('/get_cart_count')
def get_cart_count():
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            cart_count = sum(item.quantity for item in cart.items)
        else:
            cart_count = 0
    else:
        cart_count = 0
    return jsonify({'cart_count': cart_count})

# 주문 미리보기 페이지 렌더링
@web.route('/preview')
def preview():
    return render_template('web/preview.html')

# 장바구니에서 아이템을 삭제하는 API
@web.route('/remove_item/<int:item_id>', methods=['POST'])
def remove_item(item_id):
    cart_item = CartItem.query.get(item_id)
    
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        total_price = sum(item.menu.quantity * item.quantity for item in current_user.carts[0].items)
        return jsonify({'success': True, 'new_total_price': total_price})
    else:
        return jsonify({'success': False})
    
# 메뉴 항목을 검색하는 API
@web.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        results = Menu.query.filter(Menu.name.ilike(f'%{query}%')).all()
    else:
        results = []
    return render_template('web/search_results.html', results=results)
