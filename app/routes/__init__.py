from flask import Blueprint

# Initialize blueprints
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
group = Blueprint('group', __name__)
specialisation = Blueprint('specialisation', __name__)
output = Blueprint('output', __name__)

# Import routes to register them with the blueprints
from . import main, auth, group, specialisation, output
