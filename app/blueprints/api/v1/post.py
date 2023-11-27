from flask import Blueprint, request
from app.models.users import User, Address
from app.models.products import Products, Categories, ProductsCategories
from app.controllers.services.cep_finder import get_cep
from app.controllers.extensions import db, spec
from . import UsersController, CategoryController, ProductController, ProductResp
from flask_pydantic_spec import Response, Request


post_api = Blueprint('post_api', __name__, url_prefix='/api/v1')


@post_api.post('/users')
@spec.validate(
    body=Request(UsersController),
    resp=Response(HTTP_201=UsersController),
    tags=['Users']
)
def users():
    """Create a new user"""
    data = request.context.body.dict()
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


@post_api.post('/products/categories')
@spec.validate(
    body=Request(CategoryController),
    resp=Response(HTTP_200=CategoryController),
    tags=['Products']
)
def categories():
    """Create a new product category"""
    data = request.context.body.dict()

    existing_category = Categories.query.filter_by(name=data['name']).first()

    if not existing_category:
        category = Categories(
            **data
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


@post_api.post('/products')
@spec.validate(
    body=Request(ProductController),
    resp=Response(HTTP_201=ProductResp),
    tags=['Products']
)
def products():
    """Create a new product"""
    data = request.context.body.dict()
    existing_product = Products.query.filter_by(name=data['name']).first()

    if not existing_product:
        existing_category = Categories.query.filter_by(id=data['category_id']).first()
        if existing_category:
            product = Products(
                name=data['name'],
                price=data['price'],
                stock=data['stock'],
                fabricated_at=data['fabricated_at']
            )
            db.session.add(product)
            db.session.commit()

            pc = ProductsCategories(category_id=existing_category.id, product_id=product.id)
            db.session.add(pc)
            db.session.commit()

            fabricated_at = product.fabricated_at.strftime('%Y/%m/%d')

            return {
                'id': product.id,
                'category': existing_category.name,
                'name': product.name,
                'price': product.price,
                'stock': product.stock,
                'fabricated_at': fabricated_at
                }

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
