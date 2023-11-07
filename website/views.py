from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User
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
            return redirect(url_for('views.home'))
    return render_template('create_post.html', user=current_user)


@views.route("/contact")
def contact():
    return render_template('contact.html', user=current_user)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("No such post found.", category="error")
    elif current_user.id != post.author:
        flash("You don't have permission to do that.", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully.", category='success')

    return redirect(url_for('views.home'))


@views.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash("User doesn't exist.", category='error')
        return redirect(url_for('views.home'))

    posts = Post.query.filter_by(author=user.id).all()
    return render_template("posts.html", user=current_user, posts=posts, username=username)
