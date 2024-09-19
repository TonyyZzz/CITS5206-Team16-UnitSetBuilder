from flask import render_template, request
from . import main  # Import the 'main' blueprint

# Define the route for the index page
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/grouping-page')
def grouping():
    # Extract the course data from the URL parameters
    course_id = request.args.get('courseId')
    course_title = request.args.get('courseTitle')
    course_code = request.args.get('courseCode')

    # Pass these values to the template
    return render_template('grouping-page.html', course_id=course_id, course_title=course_title, course_code=course_code)



@main.route('/unit_set')
def unit_set():
    return render_template('unit_set.html')
