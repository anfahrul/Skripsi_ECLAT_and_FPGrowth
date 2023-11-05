from flask import render_template, request, redirect, url_for, flash
from app import db
from src.models.transaction import Transaction, TransactionProduct
from src.models.product import Product
import flask_excel as excel
import pandas as pd
from sqlalchemy import func


def importIndex():
    return render_template('dataset/import.html')
    

def doImportFile():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"
    
    if file:
        # Membaca file Excel menggunakan pandas
        df = pd.read_excel(file)

        for index, row in df.iterrows():
            date = row['TANGGAL']
            transaction_id = row['NO. FAKTUR']
            item_code = str(row['KODE BARANG'])
            name = row['NAMA BARANG']
            quantity = row['QTY']
            price = row['HARGA']
            # subtotal = row['SUBTOTAL']

            # Menyimpan data produk ke tabel 'product'
            existing_product = Product.query.filter_by(itemCode=item_code).first()
            if existing_product:
                existing_product.name = name
                existing_product.price = price
            else:
                product = Product(itemCode=item_code, name=name, price=price)
                db.session.add(product)

            # Menyimpan data transaksi ke tabel 'transaction'
            existing_transaction = Transaction.query.filter_by(transaction_id=transaction_id).first()
            if not existing_transaction:
                transaction = Transaction(transaction_id=transaction_id, date=date, total_price=0)  # Total harga akan dihitung nanti
                db.session.add(transaction)
                existing_transaction = transaction
            
            # Menyimpan data produk transaksi ke tabel 'transaction_products'
            existing_transaction_product = TransactionProduct.query.filter_by(transaction_id=transaction_id, itemCode=item_code).first()
            if not existing_transaction_product:
                # Jika belum ada, tambahkan data baru ke tabel 'transaction_products'
                transaction_product = TransactionProduct(transaction_id=transaction_id, itemCode=item_code, quantity=quantity)
                db.session.add(transaction_product)
                existing_transaction_product = transaction_product
              
                # Update total price  
                # subtotal_for_product = price * quantity
                # existing_transaction.total_price += subtotal
            else:
                existing_transaction_product.quantity = quantity
        
        
        # Query untuk menghitung total_price dari tabel transaction_products
        subtotal_query = db.session.query(
            TransactionProduct.transaction_id,
            func.sum(TransactionProduct.quantity * Product.price).label('subtotal')
        ).join(
            Product,
            TransactionProduct.itemCode == Product.itemCode
        ).group_by(TransactionProduct.transaction_id).subquery()

        # Update total_price di tabel transactions
        db.session.query(Transaction).filter(
            Transaction.transaction_id == subtotal_query.c.transaction_id
        ).update(
            {Transaction.total_price: subtotal_query.c.subtotal},
            synchronize_session=False
        )
         
        db.session.commit()
        
        
        dataframe_html = df.to_html(classes='table table-bordered', index=False, escape=False,
                                    render_links=True, 
                                    formatters={"header": lambda x: f'<th style="text-align: center;">{x}</th>'})
    
    flash('Dataset berhasil diimport.')
    return render_template('dataset/import.html', dataframe_html=dataframe_html)