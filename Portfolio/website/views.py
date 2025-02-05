from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for # Import necessary modules from Flask
from . import db
from flask_login import login_required, current_user # Import necessary modules from flask_login
from .models import Project # Import Note model from models.py
import json

# Create a Blueprint for view 
views = Blueprint('views', __name__)

@views.route('/') # Define the route for the home page
def home():
    return render_template('index.html') # Render the home.html template

@views.route('/projects', methods=['GET', 'POST']) # Define the route for the projects page
def projects():
    # Fetch all projects from the database
    projects = Project.query.all()
    
    return render_template('projects.html', projects=projects, user=current_user) # Render the projects.html template

@views.route('/add_project', methods=['POST', 'GET']) # Define the route for adding a new project
@login_required
def add_project():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        description = request.form.get('description')
        project_link = request.form.get('project_link')
        
        # Create a new project object
        projects = Project(name=name, description=description, project_link=project_link)
        
        # Add the project to the database
        db.session.add(projects)
        db.session.commit()
        
        #return jsonify({'message': 'Project added successfully!'})    
    return render_template('add_project.html', user=current_user) # Render the add_project.html template

#Delete a project from html page

@views.route('/delete_project/<int:id>', methods=['POST'])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    #Show all projects after deletion
    return redirect(url_for('views.projects'))