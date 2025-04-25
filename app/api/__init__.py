from app.api.budget import budget_routes
from app.api.projections import projections_routes

from app.api.health import health_routes
from app.api.errors import error_routes

PREFIX = "/api"

def api_router(app):
    
    budget_routes(app, prefix=PREFIX)
    projections_routes(app, prefix=PREFIX)
    
    health_routes(app, prefix=PREFIX)
    error_routes(app)


