from flask import render_template, request, redirect, url_for
from app import db
from src import utils
import uuid
from src.models.transaction import Transaction, TransactionProduct
from src.models.product import Product


def indexTrans():
    transactions = Transaction.query.all()
    
    return render_template('transaction/list_transaction.html', transactions=transactions)


def createTrans():
    products = Product.query.all()
    
    return render_template('transaction/create_transaction.html', products=products)


def storeTrans(): 
    new_uuid = uuid.uuid4()
    transaction_id = str(new_uuid)  
    # transaction_id = request.form.get('transaction_id')  
    date = request.form.get('date')
    
    new_transaction = Transaction(
        transaction_id = transaction_id,
        date = date,
        total_price=0,
    )
    
    db.session.add(new_transaction)
    
    item_codes = request.form.getlist('itemCode[]')
    quantities = request.form.getlist('quantity[]')
    item_prices = []
    
    for code in item_codes:
        if code == "Select...":
            continue
        
        item = Product.query.filter_by(itemCode=code).first()
        item_prices.append(item.price)
    
    total_price = 0
    for item_code, price, quantity in zip(item_codes, item_prices, quantities):
        if item_code == "Select...":
            continue
        
        new_transaction_product = TransactionProduct(itemCode=item_code, quantity=quantity)
        new_transaction.products.append(new_transaction_product)
        
        total_price += price * int(quantity)

    new_transaction.total_price = total_price
    db.session.commit()
    
    return redirect(url_for('transaction_blueprint.list_transaction'))