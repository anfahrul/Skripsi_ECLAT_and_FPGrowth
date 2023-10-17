from flask import Blueprint, render_template, request
from src.models.user import User
from src.models.product import Product
from src.controllers.productController import index, create, edit, update, delete


user_blueprint = Blueprint('user_blueprint', __name__, url_prefix='/')
product_blueprint = Blueprint('product_blueprint', __name__, url_prefix='/products')


@user_blueprint.route("/user", methods=["GET"])
def say_bye():
    return render_template('home.html')


# Product
@product_blueprint.route("/", methods=["GET", "POST"])
def list_add_product():
    if request.method == 'GET': return index()
    if request.method == 'POST': return create()
    else: return "Method not allowed"

@product_blueprint.route("/<itemCode>/edit", methods=["GET", "POST"])
def edit_product(itemCode):
    if request.method == 'GET': return edit(itemCode)
    if request.method == 'POST': return update(itemCode)
    else: return "Method not allowed"

@product_blueprint.route("/<itemCode>/delete", methods=["POST"])
def delete_product(itemCode):
    return delete(itemCode)