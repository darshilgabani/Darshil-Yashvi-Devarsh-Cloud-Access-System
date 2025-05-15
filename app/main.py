from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from .database import create_db_and_tables
from .routes import user, plans, subscriptions, token, admin, cloud_apis, permissions, usage  # ✅ Added usage

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

# Register routers
app.include_router(user.router)
app.include_router(plans.router)
app.include_router(subscriptions.router)
app.include_router(token.router)
app.include_router(admin.router)
app.include_router(cloud_apis.router)
app.include_router(permissions.router)
app.include_router(usage.router)  # ✅ Added usage router

# Swagger UI with JWT token auth config
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Yashvi-Darshil-Devarsh-Cloud Service Access Management System",
        version="0.1.0",
        description="This is a backend API with JWT token authentication.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
