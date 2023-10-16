from flask import Blueprint
from src.models.user import User


user_blueprint = Blueprint('user_blueprint', __name__, url_prefix='/')


@user_blueprint.route("/user", methods=["GET"])
def say_bye():
    return "Goodbye!"