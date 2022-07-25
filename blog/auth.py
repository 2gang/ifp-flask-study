from flask_login import login_user, logout_user, current_user, login_required
from flask import Blueprint, render_template, redirect, request, flash, url_for
from . import db 
from blog.forms import SignupForm, LoginForm
from blog.models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        password = form.password.data
        user = User.query.filter_by(email=form.email.data).first()
        
        if user:
            if check_password_hash(user.password, password):    
                #check_password_hash : 입력받은 password와 기존 password를 비교하여 참 거짓 반환
                flash("Logged in!", category='success')
                login_user(user, remember=True) #사용자 정보를 session에 저장
                return redirect(url_for('views.blog_home'))
            else:
                flash("Password is incorrect!", category='error')
        else:
            flash("Email does not exist...", category='error')
    return render_template("login.html", form=form, user=current_user)

@auth.route('/logout')
@login_required 
#특정 요청을 실행하기 전 로그인이 필요한 기능에서 요청을한 사용자가 로그인된 사용자인지 확인한다.
def logout():
    logout_user()
    #flask_login의 함수로 session 정보를 삭제한다.
    return redirect(url_for("views.blog_home"))

@auth.route('/sign-up', methods = ['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == "POST" and form.validate_on_submit():  #전송된 폼 데이터의 정합성을 점검
        signup_user = User(
            email = form.email.data,    #입력받은 데이터를 변수에 저장
            username = form.username.data,
            password = generate_password_hash(form.password1.data),
        )   #폼으로부터 검증된 데이터 받아오기
    
        email_exists = User.query.filter_by(email=form.email.data).first()
        username_exists = User.query.filter_by(username=form.username.data).first()
        #폼에서 받아온 데이터가 데이터베이스에 이미 존재하는지 확인
        #filter_by : 함수에서 ()안에 있는 조건에 맞는 데이터를 반환
        #first()인 경우 첫번째에 매칭되는 데이터만 반환/전부 받아오려면 all() 사용   
        
        if email_exists:
            flash('Email is already in use...', category = 'error')
        elif username_exists:
            flash('Username is already in use...', category = 'error')
        #이메일과 유저이름 중복 검사
        
        else:
            db.session.add(signup_user)
            db.session.commit()
            flash("User Created!")
            return redirect(url_for("views.blog_home"))
        #중복이 아니면 유저의 정보를 추가후 저장, 그리고 home으로 리다이렉트
     
    return render_template("signup.html", form=form, user=current_user)    #GET요청을 보내면 회원가입 템플릿으로 넘어감

