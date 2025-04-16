from flask import Flask
from app.routes import main

def create_app():
    # Tell Flask to look in client/html for templates
    app = Flask(__name__, template_folder='../client/html')
    app.register_blueprint(main)
    return app
