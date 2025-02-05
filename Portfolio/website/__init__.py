from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager # Import Flask-Login for user authentication

db =SQLAlchemy() # Database connection
DB_NAME = 'database.db' # Database name

def create_app():
    # Create the Flask app instance
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    bootstrap = Bootstrap5(app)
    db.init_app(app)
    
    
    #Register routes and views
    from .views import views # Import views module
    from .auth import auth # Import auth module
    
    app.register_blueprint(views, url_prefix='/') # Register the views module as a Blueprint
    app.register_blueprint(auth, url_prefix='/') # Register the auth module as a Blueprint
    
    from .models import User # Import User model from models.py
    
    
    # Check if the database file exists, if not create it
    with app.app_context():
        if not path.exists(DB_NAME):
            db.create_all() # Create tables if they don't exist yet
            
    login_manager = LoginManager() # Initial login manager
    login_manager.login_view = 'auth.login' # Define the login view
    login_manager.init_app(app) # Initialize login manager with the Flask app
    
    @login_manager.user_loader # Define the function to load user from the database
    def load_user(id): # Load user from the database
        return User.query.get(int(id)) # Return user object from the database based on id   
    return app