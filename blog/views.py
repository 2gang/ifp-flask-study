from flask import Blueprint, render_template
from flask_login import current_user
views = Blueprint("views", __name__)

@views.route('/')
@views.route('/home')
def blog_home():
    return render_template("index.html", user=current_user)

@views.route('/about')
def about():
    return render_template("about.html", user=current_user)

@views.route('/contact')
def contact():
    return render_template("contact.html", user=current_user)

@views.route('/category')
def category():
    return render_template("category.html", user=current_user)