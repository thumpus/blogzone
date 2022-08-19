"""Blogly application."""

from email.mime import image
from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogzone'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "blogz0ne"

connect_db(app)
db.create_all()

@app.route("/")
def redirect_to_users():
    """redirects to the users page (for now)"""
    return redirect("/users")

@app.route("/users")
def show_users():
    """shows the homepage"""
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/users/new", methods=["GET"])
def show_new_user_form():
    """shows the new user form"""
    return render_template("new-user-form.html")

@app.route("/users/new", methods=["POST"])
def add_user():
    """adds a user"""
    first_name = request.form['firstname']
    last_name = request.form['lastname']
    image_url = request.form['imgurl']
    if not first_name:
        flash("Please enter a first name.")
        return render_template("new-user-form.html")
    if not last_name:
        flash("Please enter a last name.")
        return render_template("new-user-form.html")
    else:
        user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(user)
        db.session.commit()
        return redirect("/users")

@app.route("/users/<int:user_id>")
def show_profile(user_id):
    """show a user's profile"""
    user = User.query.get_or_404(user_id)
    return render_template("profile.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["GET"])
def edit_user(user_id):
    user = User.query.get(user_id)
    return render_template("edit-user-form.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['firstname']
    user.last_name = request.form['lastname']
    user.image_url = request.form['imgurl']
    if not user.first_name:
        flash("Please enter a first name.")
        return render_template("edit-user-form.html", user=user)
    if not user.last_name:
        flash("Please enter a last name.")
        return render_template("edit-user-form.html", user=user)
    db.session.commit()
    return redirect(f"/users/{user.id}")

@app.route("/users//<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")
