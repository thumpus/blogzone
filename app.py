"""Blogly application."""

from email.mime import image
from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogzone'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "blogz0ne"

connect_db(app)
db.create_all()

@app.route("/")
def redirect_to_users():
    """shows the home page"""
    posts = Post.query.all()
    return render_template("home.html", posts=posts)

# USER ROUTES

@app.route("/users")
def show_users():
    """shows the users page"""
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
    """show's the edit user form"""
    user = User.query.get(user_id)
    return render_template("edit-user-form.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    """updates user info and takes you to the new user's profile"""
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
    """deletes user"""
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

# POST ROUTES

@app.route("/users/<int:user_id>/posts/new", methods=["GET"])
def new_post(user_id):
    """shows the new post form"""
    user = User.query.get_or_404(user_id)
    return render_template("new-post-form.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def submit_post(user_id):
    """submits a new post and takes you to it"""
    title = request.form["posttitle"]
    content = request.form['postbody']
    if not title:
        flash("Please enter a title for your post.")
        return render_template("new-post-form.html")
    if not content:
        flash("Please enter text for your post.")
        return render_template("new-post-form.html")
    else:
        post = Post(title=title, content=content, author=user_id)
        db.session.add(post)
        db.session.commit()
        return redirect(f"/posts/{post.id}")
    
@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """shows the post with the specified id"""
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """deletes post"""
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/")