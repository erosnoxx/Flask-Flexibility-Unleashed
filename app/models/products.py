from app.controllers.extensions import db


class Categories(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)


class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    price = db.Column(db.Float(), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    fabricated_at = db.Column(db.Date, nullable=False)

    users = db.relationship('UserProduct', backref='users', lazy=True)
    category = db.relationship('ProductsCategories', backref='category', lazy=True)

class ProductsCategories(db.Model):
    __tablename__ = 'productscategories'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)