from flask import render_template
from . import main  # Import the 'main' blueprint

# Define the route for the index page
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/grouping-page')
def grouping():
    return render_template('grouping-page.html') 

@main.route('/unit_set')
def unit_set():
    return render_template('unit_set.html')
