from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


"""Models for Blogly."""


class User(db.Model):
    """Pet."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(15),
                     nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Image_not_available.png/800px-Image_not_available.png?20210219185637"
    image_url = db.Column(db.String, nullable=True, default=20)
