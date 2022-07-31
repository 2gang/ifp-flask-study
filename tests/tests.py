import unittest
from os import path

from flask_login import current_user
from bs4 import BeautifulSoup # pip install BeautifulSoup4

from blog import create_app
from blog import db
import os

from blog.models import User

basedir = os.path.abspath(os.path.dirname(__file__))
app = create_app()
app.testing = True

'''
회원가입, 로그인, 로그아웃 부분을 테스트
1. 2명의 유저를 데이터베이스에 넣어 본 후, 데이터베이스에 들어간 유저의 수가 총 2명이 맞는지를 확인한다.
2. auth/sign-up 에서 폼을 통해서 회원가입 요청을 보낸 후, 데이터베이스에 값이 잘 들어갔는지를 확인한다.
3. 로그인 전에는 네비게이션 바에 "login", "sign up" 이 보여야 하고, 로그인한 유저 이름과 "logout" 이 표시되면 안 된다.
'''


class TestAuth(unittest.TestCase):
    # 테스트를 위한 사전 준비
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        # 테스트를 위한 db 설정
        self.db_uri = 'sqlite:///' + os.path.join(basedir, 'test.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        if not path.exists("tests/" + "test_db"):  # DB 경로가 존재하지 않는다면,
            db.create_all(app=app)  # DB를 하나 만들어낸다.

    # 테스트가 끝나고 나서 수행할 것, 테스트를 위한 데이터베이스의 내용들을 모두 삭제한다.
    def tearDown(self):
        os.remove('tests/test.db')
        self.ctx.pop()
        
                
    # 1. 2명의 유저를 데이터베이스에 넣어 본 후, 
    # 데이터베이스에 들어간 유저의 수가 총 2명이 맞는지를 확인한다.
    # def test_signup_by_database(self):
    #     self.user_test_1 = User(
    #         email="hello@example.com",
    #         username="testuserex1",
    #         password="12345",
    #         is_staff=True
    #     )
    #     db.session.add(self.user_test_1)
    #     db.session.commit()

    #     self.user_test_2 = User(
    #         email="hello2@example.com",
    #         username="testuserex2",
    #         password="12345",
    #     )
    #     db.session.add(self.user_test_2)
    #     db.session.commit()
        

    #     # 데이터베이스에 있는 유저의 수가 총 2명인가?
    #     self.assertEqual(User.query.count(), 2)
    #     #assetEqual은 TestCase 클래스가 제공하는 메소드 중 하나로 
    #     #위 코드는 데이터베이스의 존재하는 유저들의 수가 2와 같은지를 체크하는 것이다.
        
    #     db.session.close()
        
        
    # 2. auth/sign-up 에서 폼을 통해서 회원가입 요청을 보낸 후, 
    # 데이터베이스에 값이 잘 들어갔는지를 확인한다.
    def test_signup_by_form(self):
        response = self.client.post('/auth/sign-up',data=dict(email="helloworld@naver.com", 
                username="hello", password1="dkdldpvmvl", password2="dkdldpvmvl"))
        self.assertEqual(1, User().query.count())
        
        db.session.close() 
    
    # 3. 로그인 전에는 네비게이션 바에 "login", "sig up" 이 보여야 하고, 로그인한 유저 이름과 "logout" 이 표시되면 안 된다.
#     def test_before_login(self):
#         # 로그인 전이므로, 네비게이션 바에는 "login", "sign up" 이 보여야 한다.
#         response = self.client.get('/')
#         soup = BeautifulSoup(response.data, 'html.parser')
#         navbar_before_login = soup.nav  # nav 태그 선택

#         self.assertIn("Login", navbar_before_login.text)  # navbar 안에 "Login" 이 들어있는지 테스트
#         self.assertIn("Sign Up", navbar_before_login.text, )  # navbar 안에 "Sign Up" 이 들어있는지 테스트
#         self.assertNotIn("Logout", navbar_before_login.text, )  # navbar 안에 "Logout" 이 없는지 테스트

#         # 로그인을 하기 위해서는 회원가입이 선행되어야 하므로, 폼에서 회원가입을 진행해 준다.
#         response = self.client.post('/auth/sign-up',
#                                     data=dict(email="helloworld@naver.com", username="hello", password1="dkdldpvmvl",
#                                               password2="dkdldpvmvl"))
#         # 이후, auth/login 에서 로그인을 진행해 준다.
#         with self.client:
#             response = self.client.post('/auth/login',
#                                         data=dict(email="helloworld@naver.com", username="hello",
#                                                   password="dkdldpvmvl"),
#                                         follow_redirects=True)
#             soup = BeautifulSoup(response.data, 'html.parser')
#             navbar_after_login = soup.nav

#             # 로그인이 완료된 후, 네비게이션 바에는 로그인한 유저 이름과 "Logout" 이 표시되어야 한다.
#             self.assertIn(current_user.username, navbar_after_login.text)
#             self.assertIn("Logout", navbar_after_login.text)
#             # 로그인이 완료된 후, 네비게이션 바에는 "Login" 과 "Sign Up" 이 표시되면 안 된다.
#             self.assertNotIn("Login", navbar_after_login.text)
#             self.assertNotIn("Sign up", navbar_after_login.text)
            
#             db.session.close() 


# if __name__ == "__main__":
#     unittest.main()