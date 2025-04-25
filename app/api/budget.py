from flask import jsonify, request
import time

ENDPOINT = "budget"

def budget_routes(app, prefix):
    app.add_url_rule(f"{prefix}/{ENDPOINT}", f"{prefix}/{ENDPOINT}", budget, methods=["GET"])
    
def budget():
    return jsonify({"status": "budget"}), 200
