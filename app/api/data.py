from flask import jsonify, request
from app.forms import *

ENDPOINT = "data"

def data_routes(app, prefix):
    app.add_url_rule(f"{prefix}/{ENDPOINT}", f"{prefix}/{ENDPOINT}", data, methods=["GET"])
    
def data():
    return jsonify({"status": "data"}), 200
