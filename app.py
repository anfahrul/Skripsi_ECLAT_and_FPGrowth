from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate

class Base(DeclarativeBase):
  pass


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://anfahrul:pass7890@localhost:5432/sinarmartanalytics'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


from src.models.user import User
from src.models.product import Product
migrate = Migrate(app, db)

from routes import home_blueprint, user_blueprint, product_blueprint
app.register_blueprint(home_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(product_blueprint)


if __name__=="__main__":
    app.run(host="0.0.0.0")