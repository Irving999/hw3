from app import db
from app import login
from datetime import datetime
from flask_login import UserMixin

# User class 
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(32))
    email = db.Column(db.String(32))
    recipes = db.relationship('Recipe', back_populates='chef')

    # Function that sets password
    def set_password(self, password):
        self.password = password
    
    # Function that checks password
    def check_password(self, password):
        return self.password == password

# Recipe class
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key to link recipe to user
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), index=True)
    chef = db.relationship('User', back_populates='recipes')

# Load function to load user by id
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))