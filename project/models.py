from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class shop(db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    postUrl = db.Column(db.String(100))
    title = db.Column(db.String(100))
    details = db.Column(db.String(1000))
    review = db.Column(db.String(1000))
    imageUrl = db.Column(db.String(1000))

