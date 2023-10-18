from flask import render_template, request, redirect, url_for
from app import db
from src.models.product import Product


def index():
    products = Product.query.all()
    
    return render_template('product/list_product.html', products=products)


def create():
    return render_template('product/create_product.html')


def store():
    request_form = request.form.to_dict()
    
    new_item = Product(
        itemCode = request_form['itemCode'],
        name = request_form['name'],
        price = request_form['price'],
        )
    
    db.session.add(new_item)
    db.session.commit()
    
    # products = Product.query.all()
    
    # return render_template('product/list_product.html', products=products)
    return redirect(url_for('product_blueprint.list_product'))


def edit(itemCode):
    product = Product.query.get(itemCode)
    
    return render_template('product/edit_product.html', product=product)


def update(itemCode):
    request_form = request.form.to_dict()
    product = Product.query.get(itemCode)
    
    product.name = request_form['name']
    product.price = request_form['price']

    db.session.commit()
    
    return redirect(url_for('product_blueprint.list_product'))


def delete(itemCode):
    Product.query.filter_by(itemCode=itemCode).delete()
    db.session.commit()
    
    return redirect(url_for('product_blueprint.list_product'))