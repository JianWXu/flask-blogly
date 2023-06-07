"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv(override=True)
pw = os.getenv("pw")
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{pw}@localhost/blogly'

app.app_context().push()


app.config['SECRET_KEY'] = "HELLO123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def redirect_index():
    return redirect("/users")


@app.route('/users')
def home_index():
    users = User.query.all()
    return render_template("users/index.html", users=users)


@app.route('/users/new')
def add_users():
    return render_template("users/new_user.html")


@app.route('/users/new', methods=["POST"])
def add_users_post():
    create_user = User(
        first_name=request.form['fname'],
        last_name=request.form['lname'],
        image_url=request.form['url'] or None
    )
    db.session.add(create_user)
    db.session.commit()
    return redirect("/users")


@app.route('/users/<int:user_id>')
def user_details(user_id):
    user = User.query.get(user_id)
    return render_template("users/detail.html", user=user)


@app.route('/users/<int:user_id>/edit')
def edit_page(user_id):
    user = User.query.get(user_id)
    return render_template("users/edit.html", user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_page_post(user_id):
    user = User.query.get(user_id)
    user.first_name = request.form['fname_edit']
    user.last_name = request.form['lname_edit']
    user.image_url = request.form['image_edit']
    db.session.add(user)
    db.session.commit()
    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")


# Post editing and creating routes

@app.route('/users/<int:user_id>/posts/new')
def new_post_page(user_id):
    user = User.query.get(user_id)
    return render_template("/posts/new_post_form.html", user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def post_form(user_id):
    user = User.query.get(user_id)
    create_post = Post(
        title=request.form['npost-title'],
        content=request.form['npost-content'],
        user=user
    )
    db.session.add(create_post)
    db.session.commit()
    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('/posts/post_detail.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    post = Post.query.get(post_id)
    return render_template('/posts/edit_post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_form(post_id):
    post = Post.query.get(post_id)
    post.title = request.form['epost-title']
    post.content = request.form['epost-content']
    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')
