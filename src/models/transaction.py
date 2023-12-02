from app import db


class Transaction(db.Model):
    __tablename__ = 'transactions'

    transaction_id = db.Column(db.String, primary_key=True)
    date = db.Column(db.Date)
    total_price = db.Column(db.Float)
    products = db.relationship('TransactionProduct', backref='transaction', lazy='dynamic')   


    def __init__(self, transaction_id, date, total_price):
        self.transaction_id = transaction_id        
        self.date = date      
        self.total_price = total_price


    def __repr__(self):
        return f"<User {self.transaction_id}>"
    
    
class TransactionProduct(db.Model):
    __tablename__ = 'transaction_products'
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String, db.ForeignKey('transactions.transaction_id', onupdate="CASCADE", ondelete="CASCADE"))
    itemCode = db.Column(db.String, db.ForeignKey('products.itemCode', onupdate="CASCADE", ondelete="RESTRICT"))
    quantity = db.Column(db.Integer)