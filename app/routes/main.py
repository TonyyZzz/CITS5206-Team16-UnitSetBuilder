from flask import render_template
from . import main

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/grouping-page')
def grouping():
    return render_template('grouping-page.html') 
