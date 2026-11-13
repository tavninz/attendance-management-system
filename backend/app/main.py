# app/main.py
import time
from fastapi import FastAPI
from app.api.core.config import settings
from app.api.core.database import SessionLocal, engine, Base
from app.api.v1.router import api_router
from app.api.core.seed import seed_initial_users

# Initialize FastAPI app using settings from config.py
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Track server start time for uptime calculation
START_TIME = time.time()

# Automatically create database tables on startup (Development/Fast CRUD setup)
@app.on_event("startup")
def startup_event():
    # 1. Create tables
    Base.metadata.create_all(bind=engine)
    
    # 2. Seed default users
    db = SessionLocal()
    try:
        seed_initial_users(db)
    finally:
        db.close()

# Include all V1 API routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to the API. Visit /api/v1/health for system status."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)