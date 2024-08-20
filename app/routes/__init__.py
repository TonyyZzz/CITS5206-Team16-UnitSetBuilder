from flask import Blueprint

# Initialize blueprints
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

# Import routes to register them with the blueprints
from . import main, auth
