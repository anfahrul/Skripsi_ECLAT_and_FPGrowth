from flask import Blueprint, render_template, request
from src.models.user import User
from src.models.product import Product
from src.controllers.productController import index, create, store, edit, update, delete
from src.controllers.transactionController import indexTrans, createTrans, storeTrans, detailTrans

home_blueprint = Blueprint('home_blueprint', __name__, url_prefix='/')
user_blueprint = Blueprint('user_blueprint', __name__, url_prefix='/users')
product_blueprint = Blueprint('product_blueprint', __name__, url_prefix='/products')
transaction_blueprint = Blueprint('transaction_blueprint', __name__, url_prefix='/transaction')


# Home
@home_blueprint.route("/", methods=["GET"])
def home():
    return render_template('dashboard.html')


@user_blueprint.route("/", methods=["GET"])
def dashboard():
    return render_template('dashboard.html')


# Product
@product_blueprint.route("/", methods=["GET"])
def list_product():
    if request.method == 'GET': return index()
    else: return "Method not allowed"

@product_blueprint.route("/create", methods=["GET", "POST"])
def create_product():
    if request.method == 'GET': return create()
    if request.method == 'POST': return store()
    else: return "Method not allowed"

@product_blueprint.route("/<itemCode>/edit", methods=["GET", "POST"])
def edit_product(itemCode):
    if request.method == 'GET': return edit(itemCode)
    if request.method == 'POST': return update(itemCode)
    else: return "Method not allowed"

@product_blueprint.route("/<itemCode>/delete", methods=["POST"])
def delete_product(itemCode):
    return delete(itemCode)


# Transaction
@transaction_blueprint.route("/", methods=["GET"])
def list_transaction():
    return indexTrans()

@transaction_blueprint.route("/create", methods=["GET", "POST"])
def create_transaction():
    if request.method == 'GET': return createTrans()
    if request.method == 'POST': return storeTrans()
    else: return "Method not allowed"
    
    
@transaction_blueprint.route("/<transaction_id>/detail", methods=["GET"])
def detail_transaction(transaction_id):
    return detailTrans(transaction_id)