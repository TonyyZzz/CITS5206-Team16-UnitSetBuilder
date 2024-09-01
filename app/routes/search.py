from flask import Blueprint, render_template, request
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

    return render_template('search_results.html', results=results)
