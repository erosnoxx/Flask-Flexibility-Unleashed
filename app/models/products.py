from app.controllers.extensions import db


class Categories(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    products = db.relationship('Products', backref='products', lazy='Dynamic')


class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(255), db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    fabricated_at = db.Column(db.String(255))
    users = db.relationship('UserProduct', backref='users', lazy='dynamic')