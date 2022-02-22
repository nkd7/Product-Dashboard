# The __init__.py file creates and configures the app.
# It also registers the view file so the app has access to the routes.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

def create_app():
    # Create app and configure secret key for encrypted communications
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'helloworld'     # used to hash session data (don't hardcode this in production)

    # Register the views.py file so the app has access to view routes
    # Register the auth.py file so the app has access to auth routes
    from .views import views
    from.auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app