from apps.app import db
from apps.web.models import Cart, CartItem, Menu
from flask import Blueprint, render_template, redirect, url_for

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
    breadcrumb = [
        {'name': 'HOME', 'url': url_for('web.home')},  # 'HOME'은 홈페이지로 링크
        {'name': '메뉴', 'url': None}  # 현재 페이지는 URL 없이 표시
    ]
    return render_template('web/menu.html', breadcrumb=breadcrumb)
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
        {'name': 'HOME', 'url': url_for('web.home')},  # 'HOME'은 홈페이지로 링크
        {'name': '주문하기', 'url': None}  # 현재 페이지는 URL 없이 표시
    ]
    return render_template('web/order.html', breadcrumb=breadcrumb)
