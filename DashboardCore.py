# The DashboardCore.py file is the main application and starting point for the product dashboard.
# This program creates an instance of the app using the create_app() function
# The create_app() function is defined in website/__init__.py
from flask import Flask
from website import create_app
import json

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)