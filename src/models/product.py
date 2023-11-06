from app import db

class Product(db.Model):
    __tablename__ = 'products'

    itemCode = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(), nullable=False)    
    unit = db.Column(db.String(), nullable=False)    
    price = db.Column(db.Integer(), nullable=False)   
    transactions = db.relationship('TransactionProduct', backref='product', lazy='dynamic') 


    def __init__(self, itemCode, name, unit, price):
        self.itemCode = itemCode        
        self.name = name      
        self.unit = unit      
        self.price = price


    def __repr__(self):
        return f"<User {self.itemCode}>"