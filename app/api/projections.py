from flask import jsonify, request
import time

ENDPOINT = "projections"

def projections_routes(app, prefix):
    app.add_url_rule(f"{prefix}/{ENDPOINT}", "{prefix}/{ENDPOINT}", projections, methods=["GET"])
    
def projections():
    return jsonify({"status": "projections"}), 200
