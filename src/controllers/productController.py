from flask import render_template, request, redirect, url_for, flash
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
    flash('Barang baru berhasil disimpan.')
    
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
    print("itemCode", itemCode)
    product = Product.query.filter_by(itemCode=itemCode).first()
    
    if product:
        # Hapus produk berdasarkan 'itemCode'
        db.session.delete(product)
        db.session.commit()
    
    flash('Barang dengan kode {} berhasil dihapus.'.format(itemCode))
    
    return redirect(url_for('product_blueprint.list_product'))