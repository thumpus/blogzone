"""Blogly application."""

from email.mime import image
from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogzone'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "blogz0ne"

toolbar = DebugToolbarExtension(app)

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
    tags = Tag.query.all()
    return render_template("new-post-form.html", user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def submit_post(user_id):
    """submits a new post and takes you to it"""
    alltags = Tag.query.all()
    title = request.form["posttitle"]
    content = request.form['postbody']
    if not title:
        flash("Please enter a title for your post.")
        return render_template("new-post-form.html", tags=alltags)
    if not content:
        flash("Please enter text for your post.")
        return render_template("new-post-form.html", tags=alltags)
    else:
        tag_ids = [int(num) for num in request.form.getlist("tags")]
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        post = Post(title=title, content=content, author=user_id, tags=tags)
        print("Tags ID:", tag_ids, tags, post)
        db.session.add(post)
        db.session.commit()
        return redirect(f"/posts/{post.id}")
    
@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """shows the post with the specified id"""
    post = Post.query.get_or_404(post_id)
   
    return render_template("post.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["GET"])
def edit_post(post_id):
    """shows the edit form"""
    post = Post.query.get(post_id)
    tags = Tag.query.all()
    return render_template(f"edit-post-form.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def submit_post_edit(post_id):
    """submits edits to the post"""
    alltags = Tag.query.all()
    post = Post.query.get_or_404(post_id)
    post.title = request.form['posttitle']
    post.content = request.form['postbody']
    if not post.title:
        flash("Please enter a title for your post.")
        return render_template("edit-post-form.html", post=post, tags=alltags)
    if not post.content:
        flash("Please enter content for your post.")
        return render_template("edit-post-form.html", post=post, tags=alltags)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    db.session.commit()
    return redirect(f"/posts/{post.id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """deletes post"""
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/")

# TAGS ROUTES

@app.route('/tags')
def show_tags():
    """shows the tags page"""
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/new', methods=["GET"])
def show_new_tag_form():
    """shows the page to make a new tag"""
    return render_template('new-tag-form.html')

@app.route('/tags/new', methods=["POST"])
def create_tag():
    """creates the new tag"""
    name = request.form['tagname']
    if not name:
        flash("Please enter a name for your tag.")
        return render_template("new-tag-form.html")
    else:
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()
        return redirect("/tags")

@app.route('/tags/<int:tag_id>')
def show_tag_posts(tag_id):
    """shows the tag info page"""
    tag = Tag.query.get(tag_id)
    return render_template('tag-info.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["GET"])
def edit_tag(tag_id):
    """shows the tag edit page"""
    tag = Tag.query.get(tag_id)
    return render_template('edit-tag-form.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def commit_tag_edit(tag_id):
    """commits changes made to the tag"""
    tag = Tag.query.get(tag_id)
    tag.name = request.form['tagname']
    if not tag.name:
        flash ("please enter a name for your tag")
        return render_template('edit-tag-form.html', tag=tag)
    db.session.commit()
    return redirect(f"/tags/{tag.id}")

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """deletes tag"""
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")