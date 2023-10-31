from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class MiningProcess(db.Model):
    __tablename__ = 'mining_process'
    
    id = db.Column(db.Integer, primary_key=True)
    algorithm = db.Column(db.String(50))
    period_start = db.Column(db.DateTime)
    period_end = db.Column(db.DateTime)
    minimum_support = db.Column(db.Float)
    minimum_confidence = db.Column(db.Float)
    execution_time = db.Column(db.Float)
    created_at = db.Column(db.DateTime)
    
    # Define the relationship with AssociationResult
    results = relationship('AssociationResult', backref='mining_process', cascade="all, delete-orphan")
    
    
class AssociationResult(db.Model):
    __tablename__ = 'association_results'
    
    id = db.Column(db.Integer, primary_key=True)
    mining_process_id = db.Column(db.Integer, db.ForeignKey('mining_process.id', onupdate="CASCADE", ondelete="CASCADE"))
    support = db.Column(db.Float)
    confidence = db.Column(db.Float)
    lift = db.Column(db.Float)
    
    # Define the relationship with AssociationResultProduct
    products = relationship('AssociationResultProduct', backref='association_result', cascade="all, delete-orphan")
    
    
class AssociationResultProduct(db.Model):
    __tablename__ = 'association_result_products'
    
    id = db.Column(db.Integer, primary_key=True)
    association_result_id = db.Column(db.Integer, db.ForeignKey('association_results.id', onupdate="CASCADE", ondelete="CASCADE"))
    itemCode = db.Column(db.String, db.ForeignKey('products.itemCode', onupdate="CASCADE", ondelete="RESTRICT"))
    product = db.relationship('Product')
    is_antecedent = db.Column(db.Boolean)
