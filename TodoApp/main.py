
"""
This script sets up a FastAPI application with a single endpoint to retrieve all todo items from a database using SQLAlchemy ORM.
It includes database connection management, dependency injection, and a simple GET endpoint.
"""
# Since we added relative path we have to run the app from one folder up i.e, (fast_venv) PS D:\Learning_2026\FastAPI> uvicorn TodoApp.main:app --reload


# Import FastAPI and Depends for API creation and dependency injection
from fastapi import FastAPI  # FastAPI framework and dependency injection

# # Import models to access Base for metadata
from .models import Base  # To access Base for table creation
# # Import engine and SessionLocal for DB connection
from .database import engine # DB engine and session factory

from .routers import auth, todos, admin, users

# Create FastAPI app instance
app = FastAPI()  # Initialize FastAPI app
# Create all tables in the database (if not already created)
Base.metadata.create_all(bind=engine)  # Create tables from models

@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

