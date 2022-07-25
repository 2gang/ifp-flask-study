from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager    #flask_login = 로그인 기능을 쉽게 구현할 수 있도록 도와주는 라이브러리

from pprint import pprint
db = SQLAlchemy()
DB_NAME = "blog_db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "IFP"
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views
    app.register_blueprint(views, url_prefix="/")
    from .auth import auth
    app.register_blueprint(auth, url_prefix="/auth")
    
    from .models import User    #db 생성하는 함수 호출
    create_database(app)
    
    login_manager = LoginManager()  #LoginManager() 객체 생성
    login_manager.login_view = "auth.login"
    #login_manager.login_view -> 만약 로그인하지 않고 보기에 엑세스 하려고 하면 "auth.login"으로 리디렉션
    #만약 login_view 가 설정되어 있지 않으면 401오류와 함께 중단
    
    login_manager.init_app(app) #app 에 login_manager 연결
    
    @login_manager.user_loader  #사용자 정보 조회
    def load_user_by_id(id):
        return User.query.get(int(id))  #유저 id를 받아와서 그 유저의 정보를 반환
      
    return app

def create_database(app):
    if not path.exists("blog/" + DB_NAME):  #DB 경로가 있으면 호출
        db.create_all(app=app)              #없으면 생성