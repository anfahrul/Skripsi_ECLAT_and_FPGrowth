from flask import render_template, request, redirect, url_for
from app import db
from src.models.product import Product
from src.models.transaction import Transaction
from src.models.user import User
from src.models.mining import MiningProcess


def dashboardIndex():
    products = Product.query.all()
    transactions = Transaction.query.all()
    users = User.query.all()
    miningProcess = MiningProcess.query.all()
    
    return render_template('dashboard.html',
                           products=products,
                           transactions=transactions,
                           users=users,
                           miningProcess=miningProcess)