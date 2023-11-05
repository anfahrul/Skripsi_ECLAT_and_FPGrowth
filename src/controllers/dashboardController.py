from flask import render_template, request, redirect, url_for
from app import db
from src.models.product import Product
from src.models.transaction import Transaction
from src.models.user import User
from src.models.mining import MiningProcess
from flask_login import current_user


def dashboardIndex():
    products = Product.query.all()
    transactions = Transaction.query.all()
    currentUser = User.query.filter_by(email=current_user.email).first()
    users = User.query.all()
    miningProcess = MiningProcess.query.all()
    
    return render_template('dashboard.html',
                           products=products,
                           transactions=transactions,
                           currentUser=currentUser,
                           users=users,
                           miningProcess=miningProcess)