from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user

# Blueprint configuration for urls

auth = Blueprint('auth', __name__)
# Views for authentication routes
@auth.route('/login', methods=['GET', 'POST'])  # Set HTTP methods for route
def login():
    if request.method == 'POST':
        # Validate and process form data
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()  # Query user from database
        
        if user:
            if check_password_hash(user.password, password):  # Check if password matches
                # Login user and redirect to home page
                flash('Login successful.', category='success')
                login_user(user, remember=True)  # Login user and redirect to home page
                return redirect(url_for('views.home'))  # Redirect to home page
            else:
                flash('Invalid password.', category='error')
        else:
            flash('Email does not exist.', category='error')

    # Handle login logic
    return render_template('login.html',user=current_user) # Render login template with current user

@auth.route('/logout')
@login_required # Ensure user is logged in before accessing this route
def logout():
    logout_user()  # Logout user and redirect to login page
    # Handle logout logic
    return redirect(url_for('auth.login')) # Redirect to login page

@auth.route('/register', methods=['GET', 'POST']) # Set HTTP methods for route
def register():
    if request.method == 'POST':
        # Validate and process form data
        email = request.form.get('email')
        first_name = request.form.get('firstName') # Get first name
        password1 = request.form.get('password1') # Get password
        password2 = request.form.get('password2') # Get password confirmation
        
        user = User.query.filter_by(email=email).first()  # Query user from database
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be at least 4 characters long.', category='error')
        elif len(first_name) < 2:
            flash('Name must be at least 2 characters long.', category='error')
        elif password1 != password2:
            flash('Password does not match.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters long.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))  # Create new user object
            db.session.add(new_user) # Add user to database
            db.session.commit()  # Commit changes to database
            login_user(user, remember=True)  # Login user and redirect to home page
            # Save user data to database
            flash('Account created.', category='success')
            return redirect(url_for('views.home'))  # Redirect to home page after successful registration
            
    # Handle registration logic
    return render_template('register.html', user=current_user) # Render registration template with current user
    
    