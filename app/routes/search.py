from flask import Blueprint, request, jsonify
from ..models import Unit, Course, Specialisation  # Ensure Group is imported

# Existing blueprint
search = Blueprint('search', __name__)

@search.route('/search', methods=['GET'])
def search_units():
    query = request.args.get('query')

    # Try to convert the query to an integer for id search
    try:
        query_as_int = int(query)
    except ValueError:
        query_as_int = None

    # If the query is a valid integer, search by id and name
    if query_as_int is not None:
        results = Unit.query.filter((Unit.id == query_as_int) | (Unit.name.ilike(f"%{query}%"))).all()
    else:
        # Otherwise, only search by name
        results = Unit.query.filter(Unit.name.ilike(f"%{query}%")).all()

    return jsonify([result.to_dict() for result in results])

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


