from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """connect to database"""
    db.app = app
    db.init_app(app)

"""Models for Blogly."""
class User(db.Model):
    """user model"""
    def __rep__(self):
        """show info about user"""
        u = self
        return f"Name: {u.first_name} {u.last_name} ID: {u.id}"

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.String, nullable=False, default="https://icon-library.com/images/default-profile-icon/default-profile-icon-24.jpg")
