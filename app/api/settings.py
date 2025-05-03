from flask import jsonify, request
from app.forms import *

ENDPOINT = "settings"

def settings_routes(app, prefix):
    app.add_url_rule(f"{prefix}/{ENDPOINT}", f"{prefix}/{ENDPOINT}", settings, methods=["POST"])
    
def settings():
    sf = settingsform()
    if sf.validate_on_submit():
        return jsonify({"currency": sf.currency.data}), 200 #just an example
    return jsonify({"status": "csrf failed lol"}), 200