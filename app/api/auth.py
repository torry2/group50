from flask import jsonify, request, redirect
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa
from app import db
from app.models import User
from app.forms import *


ENDPOINT = "auth"

def auth_routes(app, prefix):
    app.add_url_rule(f"{prefix}/{ENDPOINT}/login", f"{prefix}/{ENDPOINT}/login", login, methods=["POST"])
    app.add_url_rule(f"{prefix}/{ENDPOINT}/register", f"{prefix}/{ENDPOINT}/register", register, methods=["POST"])
    app.add_url_rule(f"{prefix}/{ENDPOINT}/update", f"{prefix}/{ENDPOINT}/update", update, methods=["POST"])
    app.add_url_rule(f"{prefix}/{ENDPOINT}/logout", f"{prefix}/{ENDPOINT}/logout", logout, methods=["GET"])
    
    app.add_url_rule(f"{prefix}/{ENDPOINT}", f"{prefix}/{ENDPOINT}", auth, methods=["GET"])

#@login_required # example for other pages, uses "views"
def auth():
    if current_user.is_authenticated:
        return jsonify({"id": current_user.id}), 200
    return jsonify({"status": "error", "message": "No user is currently logged in."}), 401

    return jsonify({"id": current_user.id}), 200
    
def login():
    if request.method != "POST":
        return jsonify({"status": "error", "message": "Method not allowed."}), 405

    if request.is_json: # support json and wt-forms as the frontend isnt implemented yet (yes this allows for csrf bypass once implemented, but is being used for testing)
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
    else:
        form = LoginForm(request.form)
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
        else:
            return jsonify({"status": "error", "message": "Invalid form data."}), 400
    
    user = User.query.filter_by(username=username).first()
        
    if user and user.check_password(password):
        login_user(user)
        return jsonify({"status": "success", "message": "Logged in successfully."}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid username or password."}), 401

def register():
    if request.method != "POST":
        return jsonify({"status": "error", "message": "Method not allowed."}), 405
    
    if request.is_json:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
    else: 
        form = RegisterForm(request.form)
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
        else:
            return jsonify({"status": "error", "message": "Invalid form data."}), 400

    if User.query.filter_by(username=username).first(): # forced unique by the model
        return jsonify({"status": "error", "message": "Username already exists."}), 409

    new_user = User(username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"status": "success", "message": "User registered successfully."}), 201

def update():
    if request.method != "POST":
        return jsonify({"status": "error", "message": "Method not allowed."}), 405
    
    if not current_user.is_authenticated:
        return jsonify({"status": "error", "message": "User not authenticated."}), 401

    if request.is_json:
        data = request.get_json()
        new_username = data.get("username")
        new_password = data.get("password")
    else:  
        form = UpdateForm(request.form)
        if form.validate_on_submit():
            new_username = form.username.data
            new_password = form.password.data
        else:
            return jsonify({"status": "error", "message": "Invalid form data."}), 400

    if new_username:
        if User.query.filter_by(username=new_username).first():
            return jsonify({"status": "error", "message": "Username already exists."}), 409
        current_user.username = new_username

    if new_password:
        current_user.set_password(new_password)

    db.session.commit()

    return jsonify({"status": "success", "message": "User information updated successfully."}), 200

def logout():
    if current_user.is_authenticated:
        print("balls")
        logout_user()
        return jsonify({"status": "success", "message": "Logged out successfully."}), 200
    return jsonify({"status": "error", "message": "No user is currently logged in."}), 401
