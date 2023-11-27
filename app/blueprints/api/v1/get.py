from flask import Blueprint
from app.controllers.extensions import db, spec
from app.models.users import User, Address
from app.models.products import Products, Categories, ProductsCategories

get_api = Blueprint('get_api', __name__, url_prefix='/api/v1')


@get_api.get('/users')
@spec.validate(tags=['Users'])
def get_users():
    """Get all users"""
    users = User.query.all()
    all_users = []

    for user in users:
        address = Address.query.filter_by(user_id=user.id).first()
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'cep': address.zipcode,
            'address': address.address,
            'city': address.city,
            'state': address.state,
            'country': address.country,
            'latitude': address.latitude,
            'longitude': address.longitude
        }
        all_users.append(user_data)
    return {
        'Users': all_users
    }, 200


@get_api.get('/users/<int:id>')
@spec.validate(tags=['Users'])
def get_user(id):
    """Get user by id"""
    user = User.query.filter_by(id=id).first()

    if not user:
        return {
            'message': 'User not found',
            'statuscode': '404'
        }, 404

    address = Address.query.filter_by(user_id=user.id).first()

    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'cep': address.zipcode,
        'address': address.address,
        'city': address.city,
        'state': address.state,
        'country': address.country,
        'latitude': address.latitude,
        'longitude': address.longitude
    }, 200


@get_api.get('/products/categories')
@spec.validate(tags=['Products'])
def get_categories():
    """Get all categories"""
    categories = Categories.query.all()
    all_categories = []

    for category in categories:
        category_data = {
            'id': category.id,
            'name': category.name
        }
        all_categories.append(category_data)
    return {
        'Categories': all_categories
    }, 200


@get_api.get('/products')
@spec.validate(tags=['Products'])
def get_products():
    """Get all products"""
    products = Products.query.all()
    all_products = []
    for product in products:
        categoryp = ProductsCategories.query.filter_by(product_id=product.id).first()
        category = Categories.query.filter_by(id=categoryp.category_id).first()
        product_data = {
            'id': product.id,
            'category': category.name,
            'name': product.name,
            'price': product.price,
            'stock': product.stock,
            'fabricated_at': product.fabricated_at.strftime('%Y/%m/%d')
        }
        all_products.append(product_data)
    return {
        'Products': all_products
    }, 200


@get_api.get('/products/<int:id>')
@spec.validate(tags=['Products'])
def get_product(id):
    """Get product by id"""
    product = Products.query.filter_by(id=id).first()
    if not product:
        return {
           'message': 'Product not found',
           'statuscode': '404'
        }, 404
    categoryp = ProductsCategories.query.filter_by(product_id=product.id).first()
    category = Categories.query.filter_by(id=categoryp.category_id).first()
    return {
        'id': product.id,
        'category': category.name,
        'name': product.name,
        'price': product.price,
        'stock': product.stock,
        'fabricated_at': product.fabricated_at.strftime('%Y/%m/%d')
    }