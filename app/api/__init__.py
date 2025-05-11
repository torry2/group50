from app.api.auth import auth_routes
from app.api.budget import budget_routes
from app.api.projections import projections_routes
from app.api.data import data_routes
from app.api.settings import settings_routes
from app.api.health import health_routes
from app.api.errors import error_routes
from app.api.minimal_share import share_routes

PREFIX = "/api"

def api_router(app):
    
    auth_routes(app, prefix="") # simpler for use with flask-login
    budget_routes(app, prefix=PREFIX)
    projections_routes(app, prefix=PREFIX)
    data_routes(app, prefix=PREFIX)
    settings_routes(app, prefix=PREFIX)
    health_routes(app, prefix=PREFIX)
    error_routes(app)
    share_routes(app, prefix=PREFIX)


