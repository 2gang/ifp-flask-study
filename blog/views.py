from unicodedata import category
from flask import Blueprint, redirect, render_template, request, redirect, url_for, abort, flash
from flask_login import current_user, login_required
from .models import get_category_model, get_post_model, db, get_comment_model, get_contact_message_model, Post
from blog.forms import PostForm, CommentForm, ContactMessageForm
views = Blueprint("views", __name__)

@views.route('/')
@views.route('/home')
def blog_home():
    post_list = Post.query.order_by(Post.created_at.desc())
    return render_template("index.html", user=current_user, post_list=post_list)

@views.route('/admin')
def admin():
    return render_template("admin.html")

@views.route('/about')
def about():
    return render_template("about.html", user=current_user)

# 모든 카테고리들의 목록을 보여줌
@views.route("/categories-list")
def categories_list():
    categories = get_category_model().query.all()  # 모든 카테고리들을 가져오고,
    # 아래에서 context 로 그것을 추가해 준다.
    return render_template("categories_list.html", user=current_user, categories=categories)

#post-list/카테고리 id로 해당 카테고리에 속한 모든 포스트들을 보여줌
@views.route("/post-list/<int:id>")
def post_list(id):
    current_category = get_category_model().query.filter_by(id=id).first()
    posts = get_post_model().query.filter_by(category_id = id)
    return render_template("post_list.html", user=current_user, posts=posts, current_category=current_category)

@views.route('/posts/<int:id>')
def post_detail(id):
    comment_form = CommentForm()
    post = get_post_model().query.filter_by(id=id).first()
    comments = get_post_model().query.filter_by(id=id).first().comments # id에 맞는 포스트 모델을 가져와서, 해당 게시물에 달린 모든 댓글들을 가져옴
    return render_template("post_detail.html", user=current_user, post=post, comments=comments, form=comment_form)

@views.route("/create-post", methods=['GET','POST'])
@login_required
def create_post():
    if current_user.is_staff == True:
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
    else:
        return abort(403)
    
@views.route("/edit-post/<int:id>", methods=["GET", "POST"])
@login_required
def edit_post(id):
    post = get_post_model().query.filter_by(id=id).first()  # id로부터 포스트를 가져오고,
    form = PostForm()  # form 을 사용할 것이므로 가져와 준다.
    categories = get_category_model().query.all()  # category 들도 모두 가져와 준다.

    # 현재 유저는 스태프 권한을 가지고 있어야 하고, 작성자만 게시물을 수정할 수 있어야 한다.
    if current_user.is_staff == True and current_user.username == post.user.username:
        if request.method == "GET":
            return render_template("post_edit_form.html", user=current_user, post=post, categories=categories, form=form)
        elif request.method == "POST" and form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            post.category_id = int(form.category.data)
            db.session.commit()
            return redirect(url_for("views.blog_home"))
    # 스태프 권한을 가지고 있지 않거나, 게시물의 작성자가 아닐 경우 403 error를 발생시킨다.
    else:
        abort(403)
        
@login_required
@views.route("/create-comment/<int:id>", methods=['POST'])
def create_comment(id):
    form = CommentForm()
    if request.method == "POST" and form.validate_on_submit():
        comment = get_comment_model()(
            content=form.content.data,
            author_id=current_user.id,
            post_id=id
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("views.post_detail", id=id))
    
@login_required
@views.route("/edit-comment/<int:post_id>/<int:comment_id>", methods=["POST"])
def edit_comment(post_id, comment_id):
    comment = get_comment_model().query.filter_by(id=comment_id).first() # 수정할 댓글을 특정해야 한다.
    form = CommentForm() # Form으로 데이터를 받아온다.
    if current_user.username == comment.user.username:
        if form.validate_on_submit():
            comment.content = form.content.data
            db.session.commit()
            return redirect(url_for("views.post_detail", id=post_id))
        else:
            print("validation failed!")
    else:
        return abort(403)
    
    
@login_required
@views.route("/delete-post/<int:id>")
def delete_post(id):
    post=get_post_model().query.filter_by(id=id).first()    #삭제할 게시물을 특정
    if current_user.username == post.user.username:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for("views.categories_list", id=id))
    else:   #그렇지 않은 유저가 시도할 경우 에러 발생
        return abort(403)

@login_required
@views.route("/delete-comment/<int:id>")
def delete_comment(id):
    comment=get_comment_model().query.filter_by(id=id).first()    #삭제할 댓글을 특정
    if current_user.username == comment.user.username:
        db.session.delete(comment)
        db.session.commit()
        return redirect(url_for("views.categories_list", id=id))
    else:   #그렇지 않은 유저가 시도할 경우 에러 발생
        return abort(403)
    
@login_required
@views.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactMessageForm()
    # GET 요청을 받으면 폼을 띄워줘야 하고,
    if current_user.is_authenticated and request.method=="GET":
        return render_template("contact.html", user=current_user, form=form)
    elif not current_user.is_authenticated and request.method=="GET":
        flash("Login required!!!", category='error')
        return redirect(url_for("views.blog_home"))
    # POST 요청을 받으면 폼으로부터 얻어온 데이터를 처리하는 역할을 수행해야 한다.
    elif current_user.is_authenticated and request.method=="POST":
        '''
        폼에서 얻어온 데이터를 데이터베이스에 저장
        폼에서 얻어온 데이터를 이메일로 발송
        '''
        if form.validate_on_submit():
            author_id = current_user.id
            phone = form.phone.data
            message = form.message.data
            contact_message = get_contact_message_model()(
                author_id = author_id,
                phone = phone,
                message = message
            )
            db.session.add(contact_message)
            db.session.commit()
            flash("Form submitted!")
            return redirect(url_for("views.blog_home"))