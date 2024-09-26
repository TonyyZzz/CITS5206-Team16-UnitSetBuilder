from flask import Flask,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
# from flask_wtf import CSRFProtect

# Initialize the extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
bcrypt = Bcrypt()
# csrf = CSRFProtect()

def create_app(config_name):
    # Create the Flask application instance
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration settings
    app.config.from_object(Config[config_name])
    app.config.from_pyfile('config.py', silent=True)

    # Initialize the extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt = Bcrypt(app)
    # csrf.init_app(app)


    @app.before_request
    def require_login():
        # If the user is not authenticated and the endpoint is not the login page, redirect to the login page
        if not current_user.is_authenticated and request.endpoint not in ['auth.login', 'static']:
            return redirect(url_for('auth.login'))


    # Import and register blueprints
    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .routes.search import search as search_blueprint  # Register the search blueprint
    app.register_blueprint(search_blueprint)

    from .routes.group import group as group_blueprint
    app.register_blueprint(group_blueprint)

    from .routes.unit import unit as unit_blueprint
    app.register_blueprint(unit_blueprint)

    from .routes.specialisation import specialisation as specialisation_bp
    app.register_blueprint(specialisation_bp)

    with app.app_context():
        from . import models

    return app
