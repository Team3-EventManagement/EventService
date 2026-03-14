from fastapi import FastAPI
from . import models
from .database import engine
from .routes import router

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Event Management API", 
    description="Microservice for managing events. Follows clean architecture, provides REST APIs, and secures via JWT.", 
    version="1.0.0"
)

# Include API Router
app.include_router(router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Event Management Platform Microservice"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
