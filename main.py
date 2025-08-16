from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.json_api import router
from api.n8nRequestListener import router as n8n_listener_router
from api.validate_json import router as validate_json_router
from db.config.connection import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    print("Starting up...")
    init_db()
    print("Database initialized...")
    yield
    # Code to run on shutdown
    print("Shutting down...")

app = FastAPI(title="Planner APIs", version="1.0.0", lifespan=lifespan)

# Include the router from json-api with /api prefix
app.include_router(router, prefix="/api")
app.include_router(n8n_listener_router, prefix="/api")
app.include_router(validate_json_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
