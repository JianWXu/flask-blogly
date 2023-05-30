"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
# from models import db, connect_db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, create_engine
from dotenv import load_dotenv
import os

load_dotenv()
pw = os.getenv("pw")
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{pw}@/blogly"

app.app_context().push()

db = SQLAlchemy()
db.app = app
db.init_app(app)

app.config['SECRET_KEY'] = "HELLO123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# connect_db(app)
# db.create_all()
