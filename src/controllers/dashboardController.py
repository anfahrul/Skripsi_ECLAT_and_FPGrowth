from flask import render_template, request, redirect, url_for, jsonify
from app import db
from src.models.product import Product
from src.models.transaction import Transaction
from src.models.user import User
from src.models.mining import MiningProcess
from flask_login import current_user
from sqlalchemy import func


def dashboardIndex():
    lenOfproducts = Product.query.count()
    lenOftransactions = Transaction.query.count()
    currentUser = User.query.filter_by(email=current_user.email).first()
    lenOfminingProcess = MiningProcess.query.count()
    
    return render_template('dashboard.html',
                           products=lenOfproducts,
                           transactions=lenOftransactions,
                           currentUser=currentUser,
                           miningProcess=lenOfminingProcess)
    
    
def dashboardSalesData():
    results = db.session.query(
        func.to_char(Transaction.date, 'YYYY-MM-01').label('month_start_date'),
        func.count(Transaction.transaction_id).label('total_transactions')
    ).group_by('month_start_date').order_by('month_start_date').all()

    data = [{'month_start_date': result[0], 'total_transactions': result[1]} for result in results]

    return jsonify({
            'data': data,
        })