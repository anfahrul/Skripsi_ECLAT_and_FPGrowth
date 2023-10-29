from app import db

class MiningProcess(db.Model):
    __tablename__ = 'mining_process'
    
    id = db.Column(db.Integer, primary_key=True)
    algorithm = db.Column(db.String(50))
    period_start = db.Column(db.DateTime)
    period_end = db.Column(db.DateTime)
    minimum_support = db.Column(db.Float)
    minimum_confidence = db.Column(db.Float)
    execution_time = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    
class AssociationResult(db.Model):
    __tablename__ = 'association_results'
    
    id = db.Column(db.Integer, primary_key=True)
    mining_process_id = db.Column(db.Integer, db.ForeignKey('mining_process.id'))
    mining_process = db.relationship('MiningProcess', backref='association_results') 
    support = db.Column(db.Float)
    confidence = db.Column(db.Float)
    lift = db.Column(db.Float)
    
    
class AssociationResultProduct(db.Model):
    __tablename__ = 'association_result_products'
    
    id = db.Column(db.Integer, primary_key=True)
    association_result_id = db.Column(db.Integer, db.ForeignKey('association_results.id'))
    association_result = db.relationship('AssociationResult', backref='products')
    itemCode = db.Column(db.String, db.ForeignKey('products.itemCode'))
    product = db.relationship('Product')
    is_antecedent = db.Column(db.Boolean)
