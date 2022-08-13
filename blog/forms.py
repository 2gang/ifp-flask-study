from flask_wtf import FlaskForm #flask-wtf는 flask에서 form을 관리할 수 있는 기능을 제공하는 패키지
#form은 사용자로부터 정보를 입력받는 방식
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class SignupForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email()])
    #email : 필수 입력 항목이며, 이메일 형식을 유지
    #validators = 유효성 검사기, 문자열의 최대 길이와 같은 몇 가지 기준을 충족하는지 학인하고 반환한다
    #DataRequired() = 필드의 데이터가 True인지 확인하지 않으면 유효성 검사를 중지한다.
    
    username = StringField('username', validators=[DataRequired(), Length(4,30)])
    #username = 필수 입력 항목이며, 글자수가 최소 4글자부터 최대 30글자까지 허용
    
    password1 = PasswordField('password1', validators=[DataRequired(), Length(8,30)])
    EqualTo("password2", message="Password must match! XD") #두 필드값 비교
    password2 = PasswordField('password2', validators=[DataRequired()])
    #password1 : 필수 입력 항목이며, 글자수가 최소 8글자부터 최대 30글자까지 허용, password2와 값이 같아야함

class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    
class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])
    category = StringField('category', validators=[DataRequired()])
    
class CommentForm(FlaskForm):
    content = TextAreaField('content', validators=[DataRequired()])
    
class ContactMessageForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired(), Email()])
    phone = StringField('phone', validators=[DataRequired()])
    message = TextAreaField('message', validators=[DataRequired()])