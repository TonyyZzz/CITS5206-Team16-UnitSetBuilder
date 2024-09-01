from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

# Initialize the database object
db = SQLAlchemy()

# Initialize the migration object
migrate = Migrate()

def create_app(config_name):
    # Create the Flask application instance
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration settings
    app.config.from_object(Config[config_name])
    app.config.from_pyfile('config.py', silent=True)

    # Initialize the app with the database and migration objects
    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints
    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .routes.search import search as search_blueprint  # Register the search blueprint
    app.register_blueprint(search_blueprint)

    with app.app_context():
        from . import models

    return app
