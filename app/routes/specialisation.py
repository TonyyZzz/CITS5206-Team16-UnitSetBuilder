# specialisation.py
from flask import Blueprint, request, jsonify
from . import specialisation
from ..models import Specialisation, CourseSpecialisation, db  # Assuming models are imported here


# blueprint
specialisation = Blueprint('specialisation', __name__)

@specialisation.route('/add-specialisation', methods=['POST'])
def add_specialisation():
    data = request.get_json()
    course_id = data.get('course_id')
    specialization_id = data.get('specialization_id')

    if not course_id or not specialization_id:
        return jsonify(success=False, message='Course ID and Specialization ID are required.')

    # Check if the association already exists
    existing_association = CourseSpecialisation.query.filter_by(course_id=course_id, specialisation_id=specialization_id).first()
    if existing_association:
        return jsonify(success=False, message='This specialization is already associated with the course.')

    # Create the association
    course_specialisation = CourseSpecialisation(course_id=course_id, specialisation_id=specialization_id)
    db.session.add(course_specialisation)
    db.session.commit()

    return jsonify(success=True, message='Specialization updated in course successfully.')

@specialisation.route('/delete-specialisation', methods=['POST'])
def delete_specialisation():
    data = request.get_json()
    course_id = data.get('course_id')
    specialization_id = data.get('specialization_id')

    if not course_id or not specialization_id:
        return jsonify(success=False, message='Course ID and Specialization ID are required.')

    # Find the association between the course and the specialization
    course_specialisation = CourseSpecialisation.query.filter_by(course_id=course_id, specialisation_id=specialization_id).first()
    if not course_specialisation:
        return jsonify(success=False, message='Specialization not found in this course.')

    # Remove the association
    db.session.delete(course_specialisation)
    db.session.commit()

    return jsonify(success=True, message='Specialization removed from course successfully.')
