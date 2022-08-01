from sre_parse import CATEGORIES
from flask import Blueprint, render_template
from flask_login import current_user, login_required
from .models import get_category_model
views = Blueprint("views", __name__)

@views.route('/')
@views.route('/home')
def blog_home():
    return render_template("index.html", user=current_user)

@views.route('/about')
def about():
    return render_template("about.html", user=current_user)

# 모든 카테고리들의 목록을 보여줌
@views.route("/categories-list")
def categories_list():
    categories = get_category_model().query.all()  # 모든 카테고리들을 가져오고,
    # 아래에서 context 로 그것을 추가해 준다.
    return render_template("categories_list.html", user=current_user, categories=categories)

@views.route("/post-list")
def post_list():
    return render_template("post_list.html", user=current_user)

@views.route('posts/<int:id>')
def post_detail():
    return render_template("post_detail.html", user=current_user)

@views.route('/contact')
def contact():
    return render_template("contact.html", user=current_user)

@views.route("/create-post")
@login_required
def create_post():
    categories = get_category_model().query.all()
    return render_template("post_create_form.html", user=current_user, categories=categories)
