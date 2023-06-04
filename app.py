"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv(override=True)
pw = os.getenv("pw")
app = Flask(__name__)


# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:4littl3p4in4mi@localhost/blogly'
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

    # session.query(User).filter(User.id == user_id).update(
    #     {"first_name": request.form['fname_edit']},
    #     {"last_name": request.form['lname_edit']},
    #     {"image_url": request.form['image_edit']})
    db.session.add(user)
    db.session.commit()
    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.query.get(user_id)
    # User.query.filter_by(id=user_id).delete()
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")
