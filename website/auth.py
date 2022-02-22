# The auth.py file stores information about the auth routes.
# It is accessed from the __init__.py file.
from flask import Blueprint, render_template, redirect, url_for

# Create a new blueprint
auth = Blueprint("auth", __name__)

@auth.route('/')
@auth.route('/login', methods=["POST", "GET"])
def login():
    return render_template("login.html")

@auth.route('/sign-up', methods=["POST", "GET"])
def sign_up():
    return render_template("signup.html")

@auth.route('/logout', methods=["POST", "GET"])
def logout():
    return redirect(url_for("auth.login"))
