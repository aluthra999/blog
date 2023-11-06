from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Post
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
@login_required
def home():
    username = current_user.username.capitalize()
    posts = Post.query.all()
    return render_template('home.html', name=username, user=current_user, posts=posts)


@views.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == 'POST':
        text = request.form.get('text')
        title = request.form.get('title')
        if not text:
            flash("Post can't be empty!", category='error')
        elif not title:
            flash("Title can't be empty!", category='error')
        else:
            post = Post(title=title, text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post created", category='success')
    return render_template('create_post.html', user=current_user)


@views.route("/contact")
def contact():
    return render_template('contact.html', user=current_user)
