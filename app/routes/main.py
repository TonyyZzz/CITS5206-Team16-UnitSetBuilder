from flask import render_template
from flask import Flask, jsonify
from datetime import datetime
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

@main.route('/select-course')
def course():
    return render_template('select-course.html') 

@main.route('/greeting')
def greeting():
    current_hour = datetime.now().hour
    print(current_hour)
    if current_hour < 12:
        return jsonify(message="Good Morning ! Wishing you a productive day ahead ! ",
                       icon='<i class="bi bi-brightness-high-fill"></i>')
    elif 12 <= current_hour < 18:
        return jsonify(message="Good Afternoon ! Hope your day is going well ! ",
                       icon='<i class="bi bi-brightness-low-fill"></i>')
    else:
        return jsonify(message="Good evening ! Hope you had a great day ! ",
                       icon='<i class="bi bi-cloud-moon-fill"></i>')