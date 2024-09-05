from flask import Blueprint, request, jsonify
from ..models import Unit  # Import the Unit model

# Define a new blueprint for search functionality
search = Blueprint('search', __name__)

@search.route('/search', methods=['GET'])
def search_units():
    query = request.args.get('query')  # Get the search query from the URL parameters
    if query:
        # Search by Unit ID or Unit Name
        results = Unit.query.filter((Unit.id == query) | (Unit.name.ilike(f"%{query}%"))).all()
    else:
        results = []

    # Always return JSON response for search
    return jsonify([{'id': unit.id, 'name': unit.name} for unit in results])
