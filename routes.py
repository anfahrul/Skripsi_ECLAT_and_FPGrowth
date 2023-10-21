from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user
from app import bcrypt
from src.models.user import User
from src.models.product import Product
from src.models.post import Post, Category
from src.controllers.productController import index, create, store, edit, update, delete
from src.controllers.transactionController import indexTrans, createTrans, storeTrans, detailTrans
from src.controllers.authController import registerPost, loginPost
from src.controllers.userController import getProfile, editProfile, updateProfile, updatePassword
from src.controllers.datasetController import importIndex, doImportFile, doExportFile, handsonTable

auth_blueprint = Blueprint('auth_blueprint', __name__, url_prefix='/')
dashboard_blueprint = Blueprint('dashboard_blueprint', __name__)
dataset_blueprint = Blueprint('dataset_blueprint', __name__)
product_blueprint = Blueprint('product_blueprint', __name__)
transaction_blueprint = Blueprint('transaction_blueprint', __name__)
user_blueprint = Blueprint('user_blueprint', __name__)


# Authentication
@auth_blueprint.route("/", methods=["GET", "POST"])
def login():
    if request.method == 'GET': return render_template('auth/login.html')
    if request.method == 'POST': return loginPost(bcrypt)
    else: return "Method not allowed"


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET': return render_template('auth/register.html')
    if request.method == 'POST': return registerPost(bcrypt)
    else: return "Method not allowed"

@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_blueprint.login'))


# Home
@dashboard_blueprint.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template('dashboard.html')


# Import Dataset
@dataset_blueprint.route("/import", methods=["GET", "POST"])
@login_required
def do_import():
    if request.method == 'GET': return importIndex()
    if request.method == 'POST': return doImportFile()
    else: return "Method not allowed"

# @dataset_blueprint.route("/export", methods=['GET'])
# @login_required
# def doexport():
#     return doExportFile()

# @dataset_blueprint.route("/handson_view", methods=['GET'])
# @login_required
# def handson_table():
#     return handsonTable()


# Product
@product_blueprint.route("/products/", methods=["GET"])
@login_required
def list_product():
    if request.method == 'GET': return index()
    else: return "Method not allowed"

@product_blueprint.route("/products/create", methods=["GET", "POST"])
@login_required
def create_product():
    if request.method == 'GET': return create()
    if request.method == 'POST': return store()
    else: return "Method not allowed"

@product_blueprint.route("/products/<itemCode>/edit", methods=["GET", "POST"])
@login_required
def edit_product(itemCode):
    if request.method == 'GET': return edit(itemCode)
    if request.method == 'POST': return update(itemCode)
    else: return "Method not allowed"

@product_blueprint.route("/products/<itemCode>/delete", methods=["POST"])
@login_required
def delete_product(itemCode):
    return delete(itemCode)


# Transaction
@transaction_blueprint.route("/transaction/", methods=["GET"])
@login_required
def list_transaction():
    return indexTrans()

@transaction_blueprint.route("/transaction/create", methods=["GET", "POST"])
@login_required
def create_transaction():
    if request.method == 'GET': return createTrans()
    if request.method == 'POST': return storeTrans()
    else: return "Method not allowed"
    
@transaction_blueprint.route("/transaction/<transaction_id>/detail", methods=["GET"])
@login_required
def detail_transaction(transaction_id):
    return detailTrans(transaction_id)


# User
@user_blueprint.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == 'GET': return getProfile()
    if request.method == 'POST': return updatePassword(bcrypt)
    else: return "Method not allowed"

@user_blueprint.route("/profile/<user_id>/edit", methods=["GET", "POST"])
@login_required
def edit_profile(user_id):
    if request.method == 'GET': return editProfile(user_id)
    if request.method == 'POST': return updateProfile(user_id)
    else: return "Method not allowed"