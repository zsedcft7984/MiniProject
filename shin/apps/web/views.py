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
    burgers = Menu.query.filter_by(category='버거').all()  # '버거' 카테고리의 모든 항목 가져오기
    sides = Menu.query.filter_by(category='사이드').all()  # '사이드' 카테고리의 모든 항목 가져오기
    drinks = Menu.query.filter_by(category='음료').all()  # '음료' 카테고리의 모든 항목 가져오기
    if not current_user.is_authenticated:
        # 로그인되지 않았다면, 로그인 페이지로 리다이렉트하며 현재 URL을 next 파라미터로 전달
        return redirect(url_for('auth.login', next=request.url))
    # 로그인된 사용자에게 주문 페이지를 렌더링
    return render_template('web/order.html', breadcrumb=breadcrumb, burgers=burgers, sides=sides, drinks=drinks)