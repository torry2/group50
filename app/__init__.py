from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import jsonify, request

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager() #login.init_app(app)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app import models
    
    from app.api import api_router
    api_router(app)

    from app.blueprints import main
    from app import routes
    app.register_blueprint(main)

    return app