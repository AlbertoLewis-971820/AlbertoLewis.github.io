from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Define the Project model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Unique identifier for each project
    name = db.Column(db.String(100), nullable=False) # Name of the project
    description = db.Column(db.String(500), nullable=False) # Description of the project
    project_link = db.Column(db.String(200), nullable=False) # Link to the project
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # foreign key referencing the project table's id
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # unique identifier
    email = db.Column(db.String(100), unique=True, nullable=False) # email must be unique and not null
    password = db.Column(db.String(200), nullable=False) # password must not be null
    first_name = db.Column(db.String(100), nullable=False) # first name must not be null
    #projects = db.relationship('Project', backref='user') # one-to-many relationship with Note table, backref for lazy loading