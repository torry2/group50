from flask import jsonify, request
import time

ENDPOINT = "auth"

def auth_routes(app, prefix):
    app.add_url_rule(f"{prefix}/{ENDPOINT}", f"{prefix}/{ENDPOINT}", auth, methods=["GET"])
    app.add_url_rule(f"{prefix}/{ENDPOINT}/login", f"{prefix}/{ENDPOINT}/login", login, methods=["GET", "POST"])
    app.add_url_rule(f"{prefix}/{ENDPOINT}/register", f"{prefix}/{ENDPOINT}/register", register, methods=["GET", "POST"])
    app.add_url_rule(f"{prefix}/{ENDPOINT}/logout", f"{prefix}/{ENDPOINT}/logout", logout, methods=["GET"])
    
def auth():
    return jsonify({"status": "auth"}), 200

def login():
    return jsonify({"status": "auth"}), 200

def register():
    return jsonify({"status": "auth"}), 200

def logout():
    return jsonify({"status": "auth"}), 200
