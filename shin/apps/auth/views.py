# 사용자 인증 기능 엔트리포인트 만들기
from flask import Blueprint, render_template

#회원가입기능 엔드포인트만들기
from apps.app import db
from apps.auth.forms import SignUpForm, LoginForm
from apps.crud.models import User
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_user, logout_user

# blueprint 를 이용해 auth를 생성한다.
auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static"
)

# index 엔드포인트를 작성한다.
@auth.route("/")
def index():
    return render_template("auth/index.html")

# 회원가입의 화면의 엔드포인트
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    #SignUpForm을 인스턴스화 한다.
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data,
        )
        # 이메일 주소 중복체크를 한다.
        if user.is_duplicate_email():
            print("!")
            flash("지정 이메일 주소는 이미 등록되어 있습니다.")
            return redirect(url_for("auth.signup"))
        
        # 사용자 정보를 등록한다.
        db.session.add(user)
        db.session.commit()
        
        return render_template("auth/login.html", form=form)

    return render_template("auth/signup.html", form=form)

@auth.route("/login", methods=["GET" , "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 이메일 주소로부터 사용자를 취득한다
        user = User.query.filter_by(email=form.email.data).first()

        # 사용자가 존재하고 비밀번호가 일치하는 경우는 로그인을 한다.
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("web.order"))
        
        # 로그인 실패 메시지를 설정한다.
        flash("메일 주소 또는 비밀번호가 일치하지 않습니다.")
    breadcrumb = [
        {'name': 'HOME', 'url': url_for('web.home')},  # 'HOME'은 홈페이지로 링크
        {'name': '로그인', 'url': None}  # 현재 페이지는 URL 없이 표시
    ]
    return render_template("auth/login.html", form=form, breadcrumb=breadcrumb)
    


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
