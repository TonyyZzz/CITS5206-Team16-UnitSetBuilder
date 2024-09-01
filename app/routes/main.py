from flask import render_template
from . import main  # Import the 'main' blueprint

# Define the route for the index page
@main.route('/')
def index():
    return render_template('index.html')
