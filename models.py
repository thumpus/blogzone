from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    """connect to database"""
    db.app = app
    db.init_app(app)

"""Models for Blogly."""
class User(db.Model):
    """user model"""
    def __repr__(self):
        """show info about user"""
        u = self
        return f"Name: {u.first_name} {u.last_name} ID: {u.id}"

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default="https://icon-library.com/images/default-profile-icon/default-profile-icon-24.jpg")
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

class Post(db.Model):
    """post model"""
    def __repr__(self):
        """show info about da post"""
        p = self
        return f"Title {p.title} Content {p.content} ID {p.id}"

    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    author= db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)