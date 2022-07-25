from . import db 
from flask_login import UserMixin   #UserMixin = 로그인에서 수행하는 메소드에 대한 기본 구현을 제공 
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)    #유일키
    email = db.Column(db.String(150), unique=True)  #유일한 값 즉, 중복이 없도록    
    username = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    create_at = db.Column(db.DateTime(timezone=True), default=func.now()) # 생성일자,기본적으로 현재로 저장