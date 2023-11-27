from app.controllers.extensions import db
from app.controllers.services.generators import get_now


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)

    addresses = db.relationship('Address', backref='users', lazy=True)
    products = db.relationship('UserProduct', backref='products', lazy=True)


class Address(db.Model):
    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(32), nullable=False)
    state = db.Column(db.String(18), nullable=False)
    zipcode = db.Column(db.String(8), nullable=False)
    country = db.Column(db.String(6), nullable=False, default='Brazil')
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)


class UserProduct(db.Model):
    __tablename__ = 'user_product'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, nullable=False, default=1)
    date = db.Column(db.DateTime, default=get_now(), nullable=False)
