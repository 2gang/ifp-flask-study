from flask import Blueprint, redirect, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from .models import get_category_model, get_post_model, db
from blog.forms import PostForm
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

@views.route('/posts/<int:id>')
def post_detail():
    post = get_post_model().query.filter_by(id=id).first()
    return render_template("post_detail.html", user=current_user, post=post)

@views.route('/contact')
def contact():
    return render_template("contact.html", user=current_user)

@views.route("/create-post", methods=['GET','POST'])
@login_required
def create_post():
    form = PostForm()
    if request.method == "POST" and form.validate_on_submit():
        post = get_post_model()(
            title=form.title.data,
            content=form.content.data,
            category_id=form.category.data,
            author_id=current_user.id,
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("views.blog_home"))
    else:
        categories = get_category_model().query.all()
        return render_template("post_create_form.html", form=form, user=current_user, categories=categories)
