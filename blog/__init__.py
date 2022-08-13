import click
from flask.cli import with_appcontext
from flask import Flask, abort
from werkzeug.security import generate_password_hash
from wtforms import PasswordField, StringField
from wtforms.validators import InputRequired
from sqlalchemy.exc import IntegrityError

from flask import Flask, abort
from .models import DB_NAME, db, get_contact_message_model, get_user_model,get_post_model, get_category_model
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, current_user
#flask_login = 로그인 기능을 쉽게 구현할 수 있도록 도와주는 라이브러리
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from pprint import pprint

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "IFP"
    
    # DB 설정하기
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # DB 관련 추가할 설정
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
     # flask-admin
    app.config['FLASK_ADMIN_SWATCH'] = 'Darkly'
    admin = Admin(app, name='blog',
                  template_mode='bootstrap3')
    
    # flask-admin에 model 추가
    class MyUserView(ModelView):
        def is_accessible(self):
            if current_user.is_authenticated and current_user.is_staff == True:
                return True
            else:
                return abort(403)

        class CustomPasswordField(StringField):
            def populate_obj(self, obj, name):
                setattr(obj, name, generate_password_hash(self.data))

        form_extra_fields = {
            'password': CustomPasswordField('Password', validators=[InputRequired()])
        }
        form_excluded_columns = {
            'posts', 'created_at'
        }

    class MyPostView(ModelView):
        def is_accessible(self):
            if current_user.is_authenticated and current_user.is_staff == True:
                return True
            else:
                return abort(403)

        form_excluded_columns = {
            'created_at', 'comments'
        }

    class MyCategoryView(ModelView):
        def is_accessible(self):
            if current_user.is_authenticated and current_user.is_staff == True:
                return True
            else:
                return abort(403)

        form_excluded_columns = {
            'category'
        }
    
    class MyContactMessageView(ModelView):
        def is_accessible(self):
            if current_user.is_authenticated and current_user.is_staff == True:
               return True
            else:
                return abort(403) 

    admin.add_view(MyUserView(get_user_model(), db.session))  # get_user_model 로 유저 클래스를 가져옴
    admin.add_view(MyPostView(get_post_model(), db.session))
    admin.add_view(MyCategoryView(get_category_model(), db.session))
    admin.add_view(MyContactMessageView(get_contact_message_model(), db.session))
    db.init_app(app)
    
    from .views import views
    app.register_blueprint(views, url_prefix="/")
    from .auth import auth
    app.register_blueprint(auth, url_prefix="/auth")
    
    #db 생성하는 함수 호출
    create_database(app)
    
    login_manager = LoginManager()  #LoginManager() 객체 생성
    login_manager.login_view = "auth.login"
    #login_manager.login_view -> 만약 로그인하지 않고 보기에 엑세스 하려고 하면 "auth.login"으로 리디렉션
    #만약 login_view 가 설정되어 있지 않으면 401오류와 함께 중단
    
    login_manager.init_app(app) #app 에 login_manager 연결
    
    @login_manager.user_loader  #사용자 정보 조회
    def load_user_by_id(id):
        return get_user_model().query.get(int(id))  #유저 id를 받아와서 그 유저의 정보를 반환
    
    # Custom Command Line
    import click
    from flask.cli import with_appcontext
    @click.command(name="create_superuser")
    @with_appcontext
    def create_superuser():

        # 정보 입력받기
        username = input("Enter username : ")
        email = input("Enter email : ")
        password = input("Enter password : ")
        is_staff = True

        try:
            superuser = get_user_model()(
                username = username,
                email = email,
                password = generate_password_hash(password),
                is_staff = is_staff
            )
            db.session.add(superuser)
            db.session.commit()
        except IntegrityError:
            print('\033[31m' + "Error : username or email already exists.")
        print(f"User created! : {email}")

    app.cli.add_command(create_superuser)
    
    return app

def create_database(app):
    if not path.exists("blog/" + DB_NAME):  #DB 경로가 있으면 호출
        db.create_all(app=app)              #없으면 생성