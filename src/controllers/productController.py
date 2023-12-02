from flask import render_template, request, redirect, url_for, flash, jsonify
from app import db
from src.models.product import Product
from sqlalchemy import text, or_


def index():
    try:
        # Mengambil parameter paging dan sorting dari permintaan Ajax
        draw = int(request.args.get('draw', 1))
        start = int(request.args.get('start', 0))
        length = int(request.args.get('length', 10))
        order_column_index = int(request.args.get('order[0][column]', 1))
        order_dir = request.args.get('order[0][dir]', 'asc')
        search_value = request.args.get('search[value]', '')

        # Menentukan kolom apa yang dapat diurutkan
        sortable_columns = ['itemCode', 'name']
        order_column_name = sortable_columns[min(order_column_index, len(sortable_columns) - 1)]

        # Menentukan arah pengurutan
        if order_dir == 'asc':
            order_clause = f"{order_column_name} ASC"
        else:
            order_clause = f"{order_column_name} DESC"

        # Mengambil data untuk halaman tertentu dengan paging dan sorting
        query = Product.query.filter(
            or_(
                Product.itemCode.ilike(f"%{search_value}%"),
                Product.name.ilike(f"%{search_value}%"),
            )
        )
        
        total_records = query.count()
        productsData = query.order_by(text(order_clause)).offset(start).limit(length).all()

        products = []
        for transaction in productsData:
            products.append({
                'Kode Barang': transaction.itemCode,
                'Nama Barang': transaction.name,
            })

        return jsonify({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': total_records,
            'data': products,
        })
    except Exception as e:
        print(f"Error in index: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500


def create():
    return render_template('product/create_product.html')


def store():
    request_form = request.form.to_dict()
    
    new_item = Product(
        itemCode = request_form['itemCode'],
        name = request_form['name'],
        # price = request_form['price'],
        price = 0,
        unit=""
        )
    
    db.session.add(new_item)
    db.session.commit()
    
    flash('Barang baru berhasil disimpan.')
    
    return redirect(url_for('product_blueprint.list_product'))


def edit(itemCode):
    product = Product.query.get(itemCode)
    
    return render_template('product/edit_product.html', product=product)


def update(itemCode):
    request_form = request.form.to_dict()
    product = Product.query.get(itemCode)
    
    product.name = request_form['name']
    # product.price = request_form['price']
    product.price = 0

    db.session.commit()
    
    flash('Barang dengan kode \'{}\' berhasil diperbarui.'.format(product.itemCode))
    
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