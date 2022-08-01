import unittest
from os import path

from flask_login import current_user
from bs4 import BeautifulSoup # pip install BeautifulSoup4

from blog import create_app
from blog import db
import os

from blog.models import get_user_model, get_post_model, get_category_model

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
    def test_signup_by_database(self):
        self.user_test_1 = get_user_model()(
            email="hello@example.com",
            username="testuserex1",
            password="12345",
            is_staff=True
        )
        db.session.add(self.user_test_1)
        db.session.commit()

        self.user_test_2 = get_user_model()(
            email="hello2@example.com",
            username="testuserex2",
            password="12345",
        )
        db.session.add(self.user_test_2)
        db.session.commit()
        

        # 데이터베이스에 있는 유저의 수가 총 2명인가?
        self.assertEqual(get_user_model().query.count(), 2)
        #assetEqual은 TestCase 클래스가 제공하는 메소드 중 하나로 
        #위 코드는 데이터베이스의 존재하는 유저들의 수가 2와 같은지를 체크하는 것이다.
        
        db.session.close()
        
        
    # 2. auth/sign-up 에서 폼을 통해서 회원가입 요청을 보낸 후, 
    # 데이터베이스에 값이 잘 들어갔는지를 확인한다.
    def test_signup_by_form(self):
        response = self.client.post('/auth/sign-up',data=dict(email="helloworld@naver.com", 
                username="hello", password1="dkdldpvmvl", password2="dkdldpvmvl"))
        self.assertEqual(1, get_user_model().query.count())
        
        db.session.close() 
    
    # 3. 로그인 전에는 네비게이션 바에 "login", "sig up" 이 보여야 하고, 로그인한 유저 이름과 "logout" 이 표시되면 안 된다.
    def test_before_login(self):
        # 로그인 전이므로, 네비게이션 바에는 "login", "sign up" 이 보여야 한다.
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        navbar_before_login = soup.nav  # nav 태그 선택

        self.assertIn("Login", navbar_before_login.text)  # navbar 안에 "Login" 이 들어있는지 테스트
        self.assertIn("Sign Up", navbar_before_login.text, )  # navbar 안에 "Sign Up" 이 들어있는지 테스트
        self.assertNotIn("Logout", navbar_before_login.text, )  # navbar 안에 "Logout" 이 없는지 테스트

        # 로그인을 하기 위해서는 회원가입이 선행되어야 하므로, 폼에서 회원가입을 진행해 준다.
        response = self.client.post('/auth/sign-up',
                                    data=dict(email="helloworld@naver.com", username="hello", password1="dkdldpvmvl",
                                              password2="dkdldpvmvl"))
        # 이후, auth/login 에서 로그인을 진행해 준다.
        with self.client:
            response = self.client.post('/auth/login',
                                        data=dict(email="helloworld@naver.com", username="hello",
                                                  password="dkdldpvmvl"),
                                        follow_redirects=True)
            soup = BeautifulSoup(response.data, 'html.parser')
            navbar_after_login = soup.nav

            # 로그인이 완료된 후, 네비게이션 바에는 로그인한 유저 이름과 "Logout" 이 표시되어야 한다.
            self.assertIn(current_user.username, navbar_after_login.text)
            self.assertIn("Logout", navbar_after_login.text)
            # 로그인이 완료된 후, 네비게이션 바에는 "Login" 과 "Sign Up" 이 표시되면 안 된다.
            self.assertNotIn("Login", navbar_after_login.text)
            self.assertNotIn("Sign up", navbar_after_login.text)
            
            db.session.close()
             
class TestPostwithCategory(unittest.TestCase):
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
    
    '''
    1. 임의의 카테고리를 넣어본 후, 데이터베이스에 카테고리가 잘 추가되어 있는지 확인한다.
    2. 카테고리를 넣은 후, /categories-list 에 접속했을 때, 넣었던 카테고리들이 잘 추가되어 있는지 확인한다. 
    3. 게시물을 작성할 때에, 로그인하지 않았다면 접근이 불가능해야 한다.
    4. 임의의 카테고리를 넣어본 후,
        웹 페이지에서 폼으로 게시물을 추가할 때에 option 태그에 값이 잘 추가되는지,
        게시물을 추가한 후 게시물은 잘 추가되어 있는지
        저자는 로그인한 사람으로 추가되어 있는지 확인한다.

    '''

    def test_add_category_and_post(self):
        # 이름 = "python" 인 카테고리를 하나 추가하고,
        self.python_category = get_category_model()(
            name="python"
        )
        db.session.add(self.python_category)
        db.session.commit()
        self.assertEqual(get_category_model().query.first().name, "python")  # 추가한 카테고리의 이름이 "python" 인지 확인한다.
        self.assertEqual(get_category_model().query.first().id, 1)  # id는 1로 잘 추가되어있는지 확인한다.

        # 이름 = "rust" 인 카테고리를 하나 추가하고,
        self.rust_category = get_category_model()(
            name="rust"
        )
        db.session.add(self.rust_category)
        db.session.commit()
        self.assertEqual(get_category_model().query.filter_by(id=2).first().name,
                         "rust")  # id가 2인 카테고리의 이름이 "rust" 인지 확인한다.

        # 이름 = "javascript" 인 카테고리를 하나 더 추가해 주자.
        self.rust_category = get_category_model()(
            name="javascript"
        )
        db.session.add(self.rust_category)
        db.session.commit()


        # 카테고리 리스트 페이지에 접속했을 때에, 추가했던 3개의 카테고리가 잘 추가되어 있는지?
        response = self.client.get('/categories-list')
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIn('python', soup.text)
        self.assertIn('rust', soup.text)
        self.assertIn('javascript', soup.text)

        # 로그인 전에는, 포스트 작성 페이지에 접근한다면 로그인 페이지로 이동해야 한다. 리디렉션을 나타내는 상태 코드는 302이다.
        response = self.client.get('/create-post', follow_redirects=False)
        self.assertEqual(302, response.status_code)

       # 게시물의 작성자 생성
        response = self.client.post('/auth/sign-up',
                                    data=dict(email="helloworld@naver.com", username="hello", password1="dkdldpvmvl",
                                              password2="dkdldpvmvl"))

        # 위에서 만든 유저로 로그인
        with self.client:
            response = self.client.post('/auth/login',
                                        data=dict(email="helloworld@naver.com", username="hello",
                                                  password="dkdldpvmvl"),
                                        follow_redirects=True)
            # 로그인한 상태로, 게시물 작성 페이지에 갔을 때에 폼이 잘 떠야 한다.
            response = self.client.get('/create-post')
            self.assertEqual(response.status_code, 200) # 서버에 get 요청을 보냈을 때에, 정상적으로 응답한다는 상태 코드인 200을 돌려주는가?

            # 미리 작성한 카테고리 3개가 셀렉트 박스의 옵션으로 잘 뜨고 있는가?
            soup = BeautifulSoup(response.data, 'html.parser')
            select_tags = soup.find(id='category')
            self.assertIn("python", select_tags.text)
            self.assertIn("rust", select_tags.text)
            self.assertIn("javascript", select_tags.text)

            response_post = self.client.post('/create-post',
                                        data=dict(title="안녕하세요, 첫 번째 게시물입니다.",
                                                  content="만나서 반갑습니다!",
                                                  category="1"),
                                        follow_redirects=True)
            self.assertEqual(1, get_post_model().query.count()) # 게시물을 폼에서 작성한 후, 데이터베이스에 남아 있는 게시물의 수가 1개가 맞는가?

        # 게시물은 잘 추가되어 있는지?
        response = self.client.get(f'/posts/1')
        soup = BeautifulSoup(response.data, 'html.parser')

        # 게시물의 페이지에서 우리가 폼에서 입력했던 제목이 잘 나타나는지?
        title_wrapper = soup.find(id='title-wrapper')
        self.assertIn("안녕하세요, 첫 번째 게시물입니다.", title_wrapper.text)

        # 게시물 페이지에서, 로그인했던 유저의 이름이 저자로 잘 표시되는지?
        author_wrapper = soup.find(id='author-wrapper')
        self.assertIn("hello", author_wrapper.text)

        db.session.close()

if __name__ == "__main__":
    unittest.main()