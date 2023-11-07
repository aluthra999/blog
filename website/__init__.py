from flask import Flask
from os import path
from flask_login import LoginManager
from .database import db  # Import the db object from database.py
from .models import User, Post, Comment
from .views import views
from .auth import auth

DB_NAME = "blog.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'helloworld'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    app.static_folder = 'static'

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    @app.route('/create_database')
    def create_database():
        if not path.exists("website/" + DB_NAME):
            with app.app_context():
                db.create_all()
                print('Created database!')
        return 'Database created'

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
