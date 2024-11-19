# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the database instance
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')  # Load config from config.py
    db.init_app(app)

    # Register blueprints (separate routes in routes.py)
    from .routes import main
    app.register_blueprint(main)

    return app
