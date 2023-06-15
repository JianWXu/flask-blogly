from flask_sqlalchemy import SQLAlchemy
# import app
from datetime import datetime
from sqlalchemy import DateTime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


"""Models for Blogly."""
default_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Image_not_available.png/800px-Image_not_available.png?20210219185637"


class User(db.Model):
    """Pet."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(15),
                           nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    image_url = db.Column(db.String, nullable=False,
                          default=default_image
                          )


class Post(db.Model):
    """Post."""
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(25), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(DateTime(timezone=True),
                           default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', lazy='subquery', backref='posts')


class Tag(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    posts = db.relationship('Post', secondary='posttags', backref='tags')


class PostTag(db.Model):

    __tablename__ = "posttags"

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
