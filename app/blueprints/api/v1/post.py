from flask import Blueprint, request, jsonify
from app.models.users import User, Address
from app.models.products import Products, Categories
from app.controllers.services.cep_finder import get_cep
from app.controllers.extensions import db

api = Blueprint('api', __name__, url_prefix='/api/v1')


@api.post('/users')
def users():
    """Create a new user"""
    data = request.json
    existing_email = User.query.filter_by(email=data['email']).first()
    if not existing_email:
        user = User(
            name=data['name'],
            email=data['email'],
        )
        db.session.add(user)
        db.session.commit()

        cep = data['cep']

        address_infos = get_cep(cep)

        address = Address(user_id=user.id, **address_infos)
        db.session.add(address)
        db.session.commit()

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
        }, 201
    else:
        return {
            'message': 'Email already exists',
            'statuscode': '409'
        }, 409


@api.post('/products/categories')
def categories():
    """Create a new product category"""
    data = request.json

    existing_category = Categories.query.filter_by(name=data['name']).first()

    if not existing_category:
        category = Categories(
            name=data['name']
        )
        db.session.add(category)
        db.session.commit()

        return {
            'id': category.id,
            'name': category.name
        }, 201
    else:
        return {
            'message': 'Category already exists',
            'statuscode': '409'
        }, 409


@api.post('/products')
def products():
    """Create a new product"""
    data = request.json
    existing_product = Products.query.filter_by(name=data['name']).first()
    if not existing_product:
        existing_category = Categories.query.filter_by(id=data['category_id']).first()
        if existing_category.id:
            product = Products(
                name=data['name'],
                price=data['price'],
                description=data['description'],
                category_id=data['category_id']
            )
            db.session.add(product)
            db.session.commit()
            return {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'category_id': product.category_id
                }, 201
        else:
            return {
                'message': 'Category not found',
                'statuscode': '404'
            }, 404
    else:
        return {
           'message': 'Product already exists',
           'statuscode': '409'
        }, 409
