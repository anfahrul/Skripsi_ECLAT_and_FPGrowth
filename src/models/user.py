from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(), unique=True, nullable=False)  
    password = db.Column(db.String(100))  
    name = db.Column(db.String(100))
    created_at = db.Column(db.Date, nullable=False)
    # role = db.Column(db.String(), default="employee")    

    # __table_args__ = (
    #     db.CheckConstraint(role.in_(['student', 'teacher', 'employee']), name='role_types'),      
    # )


    def __init__(self, email, password, name, created_at):
        self.email = email
        self.password = password
        self.name = name
        self.created_at = created_at        
    
    def register_user_if_not_exist(self):        
        db_user = User.query.filter(User.email == self.email).all()
        if not db_user:
            db.session.add(self)
            db.session.commit()
        
        return True
    
    # def get_by_username(username):        
    #     db_user = User.query.filter(User.username == username).first()
    #     return db_user

    def __repr__(self):
        return f"<User {self.email}>"