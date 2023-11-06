from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        user_email = User.query.filter_by(email=email).first()
        user_username = User.query.filter_by(username=username).first()
        # If the user exists in either by their email or username
        if user_username:
            if check_password_hash(user_username.password, password):
                flash('Logged in!', category='success')
                login_user(user_username, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password', category='error')
        else:
            flash('User does not exist', category='error')

    return render_template('login.html', user=current_user)


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash("Email already exists! Please log in instead.", category='error')
        elif username_exists:
            flash("Username already exists! Please try another one.",
                  category='error')
        elif password1 != password2:
            flash("Passwords don't match! Try again.", category='error')
        elif len(username) < 2:
            flash("Username is too short! Try again.", category='error')
        elif len(password1) < 6:
            flash(
                "Password is too short! Make it at least six characters long.", category='error')
        elif len(email) < 4:
            flash("Invalid Email Address! Try Again.", category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("User Created")
            return redirect(url_for('views.home'))

    return render_template('signup.html', user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))


@auth.route("/contact")
def contact():
    return render_template('contact.html')
