from flask import Blueprint, request, jsonify
from ..models import Unit, Course, Specialisation  # Ensure Group is imported

# Existing blueprint
search = Blueprint('search', __name__)

@search.route('/search', methods=['GET'])
def search_units():
    query = request.args.get('query')
    if query:
        results = Unit.query.filter((Unit.id == query) | (Unit.name.ilike(f"%{query}%"))).all()
    else:
        results = []
    return jsonify([{'id': unit.id, 'name': unit.name} for unit in results])

# Route for course search
@search.route('/search_courses', methods=['GET'])
def search_courses():
    query = request.args.get('query', '')
    if query:
        results = Course.query.filter(Course.title.ilike(f"%{query}%")).all()
        courses = [{'id': course.id, 'code': course.code, 'title': course.title} for course in results]
        return jsonify(courses)
    return jsonify([])

# New route for group specialisation
@search.route('/search_specialisations', methods=['GET'])
def search_specialisations():
    query = request.args.get('query', '')
    if query:
        results = Specialisation.query.filter(Specialisation.name.ilike(f"%{query}%")).all()
        groups = [{'id': spec.id, 'name': spec.name} for spec in results]
        return jsonify(groups)
    return jsonify([])


