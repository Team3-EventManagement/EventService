import time
from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
from . import models
from .database import engine
from .routes import router

# Retry loop for Database initialization
MAX_RETRIES = 5
for i in range(MAX_RETRIES):
    try:
        # Create the database tables
        models.Base.metadata.create_all(bind=engine)
        print("Successfully connected to the database and created tables!")
        break
    except OperationalError as e:
        print(f"Database not ready yet (Attempt {i+1}/{MAX_RETRIES}). Waiting 3 seconds...")
        time.sleep(3)
else:
    raise Exception("Could not connect to the database after several retries.")


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
