from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
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


@views.route("/user-profile/<username>")
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User doesn't exist.", category='error')
        return redirect(url_for('views.home'))

    return render_template('user_profile.html', user=username)


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

    posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)


@views.route("/create-comment/<post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash("Comment can not be empty.", category='warning')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash("No such post found.", category='error')
            return redirect(url_for('views.home'))

    return redirect(url_for('views.home'))


@views.route("/delete-comment/<id>")
@login_required
def delete_commentt(id):
    comment = Comment.query.filter_by(id=id).first()

    if not comment:
        flash("No such comment found.", category="error")
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash("You don't have permission to do that.", category="error")
    else:
        db.session.delete(comment)
        db.session.commit()
        flash("Comment deleted successfully.", category='success')

    return redirect(url_for('views.home'))


@views.route("/like-post/<post_id>", methods=["GET"])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id)
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(post_id=post_id, author=current_user.id)
        db.session.add(like)
        db.session.commit()

    return redirect(url_for('views.home'))
