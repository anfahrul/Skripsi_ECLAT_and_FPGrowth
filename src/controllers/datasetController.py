from flask import render_template, request, redirect, url_for, flash
from app import db
from src.models.transaction import Transaction, TransactionProduct
from src.models.product import Product
import flask_excel as excel
import pandas as pd
from sqlalchemy import func
from datetime import datetime


def importIndex():
    return render_template('dataset/import.html')
    

def doImportFile():
    try:
        if 'file' not in request.files:
            return "No file part"
        
        file = request.files['file']
        
        if file.filename == '':
            return "No selected file"
        
        if file:
            # Membaca file Excel menggunakan pandas
            df = pd.read_excel(file)

            for index, row in df.iterrows():
                transaction_id = str(row['No. Faktur'])
                date = row['Tanggal Transaksi']
                
                # date_str = date.strftime('%d/%m/%Y')
                # start_date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                # start_date_iso_format = start_date_obj.strftime('%Y-%m-%d')
                
                date_str = row['Tanggal Transaksi']
                start_date_iso_format = datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')

                
                item_code = str(row['Kode Barang'])
                name = row['Nama Barang']
                # unit = row['SATUAN']
                # quantity = row['QTY']
                # price = row['HARGA']
                # subtotal = row['SUBTOTAL']

                # Menyimpan data produk ke tabel 'product'
                existing_product = Product.query.filter_by(itemCode=item_code).first()
                if existing_product:
                    existing_product.name = name
                    existing_product.unit = 0
                    existing_product.price = 0
                else:
                    product = Product(itemCode=item_code, name=name, unit=0, price=0)
                    db.session.add(product)

                # Menyimpan data transaksi ke tabel 'transaction'
                existing_transaction = Transaction.query.filter_by(transaction_id=transaction_id).first()
                if not existing_transaction:
                    transaction = Transaction(transaction_id=transaction_id, date=start_date_iso_format, total_price=0)  # Total harga akan dihitung nanti
                    db.session.add(transaction)
                    existing_transaction = transaction
                else:
                    existing_transaction.date = start_date_iso_format
                
                # Menyimpan data produk transaksi ke tabel 'transaction_products'
                existing_transaction_product = TransactionProduct.query.filter_by(transaction_id=transaction_id, itemCode=item_code).first()
                if not existing_transaction_product:
                    # Jika belum ada, tambahkan data baru ke tabel 'transaction_products'
                    transaction_product = TransactionProduct(transaction_id=transaction_id, itemCode=item_code, quantity=0)
                    db.session.add(transaction_product)
                    existing_transaction_product = transaction_product
                
                    # Update total price  
                    # subtotal_for_product = price * quantity
                    # existing_transaction.total_price += subtotal
                else:
                    existing_transaction_product.quantity = 0
            
            
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
        
        flash('Data transaksi penjualan berhasil diimport.')
        
    except Exception as e:
        flash(f'Error: {str(e)}')
        # flash(f'File tidak sesuai ketentuan, periksa kembali format file dan nama kolom.')
        dataframe_html = None
        
    return render_template('dataset/import.html', dataframe_html=dataframe_html)