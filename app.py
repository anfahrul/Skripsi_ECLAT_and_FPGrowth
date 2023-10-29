from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from flask_login import LoginManager
import flask_excel as excel

class Base(DeclarativeBase):
  pass


app = Flask(__name__)
app.secret_key = "iniSangatRahasia"
bcrypt = Bcrypt(app)
excel.init_excel(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://anfahrul:pass7890@localhost:5432/sinarmartanalytics'
db = SQLAlchemy(model_class=Base)


from src.models.user import User
from src.models.product import Product
from src.models.transaction import Transaction, TransactionProduct
from src.models.mining import MiningProcess, AssociationResult, AssociationResultProduct
migrate = Migrate(app, db)


login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

from routes import auth_blueprint, dashboard_blueprint, dataset_blueprint, user_blueprint, product_blueprint, transaction_blueprint, mining_blueprint, mining_history_blueprint
app.register_blueprint(auth_blueprint)
app.register_blueprint(dashboard_blueprint)
app.register_blueprint(dataset_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(product_blueprint)
app.register_blueprint(transaction_blueprint)
app.register_blueprint(mining_blueprint)
app.register_blueprint(mining_history_blueprint)
  
  
if __name__=="__main__":
    app.run(host="0.0.0.0")