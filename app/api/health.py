from flask import jsonify, request
import time

ENDPOINT = "health"

def health_routes(app, prefix):
    app.add_url_rule(f'{prefix}/{ENDPOINT}', 'healthcheck', healthcheck, methods=['GET'])
    app.add_url_rule(f'{prefix}/{ENDPOINT}/ping', 'ping', ping, methods=['GET'])

def healthcheck():
    return jsonify({"status": "OK"}), 200

def ping():
    start_time = time.time()
    time.sleep(0.1)  
    response_time = (time.time() - start_time) * 1000  
    return jsonify({"pong": response_time}), 200
