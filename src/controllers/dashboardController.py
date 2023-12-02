from flask import render_template, request, redirect, url_for
from app import db
from src.models.product import Product
from src.models.transaction import Transaction
from src.models.user import User
from src.models.mining import MiningProcess
from flask_login import current_user


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