from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.json_api import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    print("Starting up...")
    yield
    # Code to run on shutdown
    print("Shutting down...")

app = FastAPI(title="Planner APIs", version="1.0.0", lifespan=lifespan)

# Include the router from json-api with /api prefix
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
