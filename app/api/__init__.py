from app.api.health import health_routes
from app.api.errors import error_routes

PREFIX = "/api"

def api_router(app):
    health_routes(app, prefix=PREFIX)
    error_routes(app)


