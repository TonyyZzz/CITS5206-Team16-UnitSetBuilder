from flask import render_template, request
from . import main  # Import the 'main' blueprint
from ..models import Course, UnitSet, Specialisation, CourseSpecialisation, Group
from .. import db


# Define the route for the index page
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/grouping-page/')
def grouping():
    course_id = request.args.get('courseId')

    # Fetch the course data using the course_id
    course = Course.query.get_or_404(course_id)
    
    # Get all UnitSets associated with the course
    unit_set = UnitSet.query.filter_by(course_id=course_id).first()
    if not unit_set:
        # Create a UnitSet with default values if it does not exist
        unit_set = UnitSet(
            title=f'{course.title} Unit Set', 
            description=f'Default description for the Unit Set of {course.title}.', 
            note=f'Default note for the Unit Set of {course.title}.', 
            course_id=course_id
        )
        db.session.add(unit_set)
        db.session.commit()
    

    # Get all Specialisations associated with the course
    # Assuming that you have a relationship through the CourseSpecialisation table
    specialisations = Specialisation.query.join(CourseSpecialisation).filter(CourseSpecialisation.course_id == course_id).all()

    # Pass these values to the template
    return render_template('grouping-page.html', course=course, unit_set=unit_set, specialisations=specialisations)



@main.route('/unit_set')
def unit_set():
    item_type = request.args.get('type')
    item_id = request.args.get('id')
    if not item_type or not item_id:
        return "Error: Type and ID are required", 400

    if item_type == 'unitset':
        # Fetch unit set data using item_id
        unit_set = UnitSet.query.get(item_id)
        unit_setData = unit_set.to_dict()
        course = unit_set.course
        courseData = course.to_dict()

        groups = Group.query.filter_by(unit_set_id=item_id).all()

        return render_template('unit_set.html', item=unit_setData, type='unitset', course = courseData, groups = groups)
    
    elif item_type == 'specialisation':
        # Fetch specialization data using item_id
        specialisation = Specialisation.query.get(item_id)
        specialisationData = [specialisation.to_dict()]
        course_specialisation = CourseSpecialisation.query.filter_by(specialisation_id=item_id).first()
        if course_specialisation:
            course = Course.query.get(course_specialisation.course_id)
            courseData = course.to_dict()

        groups = Group.query.filter_by(unit_set_id=item_id).all()

        return render_template('unit_set.html', item=specialisationData, type='specialisation', course = courseData, courseData=courseData, groups = groups)
    
    else:
        return "Error: Invalid type", 400
