from website import db
from flask_login import UserMixin, current_user, login_required
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    posts = db.relationship('Post', backref='user', passive_deletes=True)


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.Integer(), db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
