
"""
This script sets up a FastAPI application with a single endpoint to retrieve all todo items from a database using SQLAlchemy ORM.
It includes database connection management, dependency injection, and a simple GET endpoint.
"""

# Import FastAPI and Depends for API creation and dependency injection
from fastapi import APIRouter, Depends, HTTPException, Path  # FastAPI framework and dependency injection
# Import Session for database session management
from sqlalchemy.orm import Session  # SQLAlchemy session for DB operations
# Import the Todos model from models.py
from models import Todos  # ORM model for todo items
# Import Annotated for type hinting with dependencies
from typing import Annotated  # For advanced type hints
# Import engine and SessionLocal for DB connection
from database import SessionLocal  # DB engine and session factory
from starlette import status
from pydantic import BaseModel, Field

from .auth import get_current_user

# Create FastAPI app instance
router = APIRouter()  # Initialize FastAPI app

# Dependency function to get a database session
def get_db():  # Provides a database session to endpoints
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Yield the session to the endpoint
    finally:
        db.close()  # Ensure the session is closed after use

# Define a dependency annotation for injecting the DB session
db_dependency = Annotated[Session, Depends(get_db)]  # Type alias for dependency injection

user_dependency=Annotated[dict,Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


# Define the root endpoint to read all todos
@router.get("/", status_code=status.HTTP_200_OK)  # HTTP GET endpoint at root URL
async def read_all(user: user_dependency,db: db_dependency):  # Inject DB session dependency
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).filter(Todos.owner_id==user.get('id')).all()  # Query all todo items and return as response

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency,db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model=db.query(Todos)\
        .filter(Todos.owner_id==user.get('id'))\
        .filter(Todos.id==todo_id).first()
    
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code= 404, detail= 'Todo not found.')


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency,db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(staus_code=401, detail='Authentication failed')
    
    todo_model=Todos(**todo_request.model_dump(),owner_id=user.get('id'))
    # print(todo_model)
    db.add(todo_model)
    db.commit()

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency,  todo_request: TodoRequest, todo_id: int= Path(gt=0)):
   
    if user is None:
        raise HTTPException(staus_code=401, detail='Authentication failed')
    todo_model=db.query(Todos)\
        .filter(Todos.owner_id==user.get('id'))\
            .filter(Todos.id==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    todo_model.title=todo_request.title
    todo_model.description=todo_request.description
    todo_model.priority=todo_request.priority
    todo_model.complete=todo_request.complete
    db.add(todo_model)
    db.commit()

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(staus_code=401, detail='Authentication failed')
    todo_model=db.query(Todos)\
        .filter(Todos.owner_id==user.get('id'))\
        .filter(Todos.id==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    db.query(Todos)\
        .filter(Todos.owner_id==user.get('id'))\
        .filter(Todos.id==todo_id).delete()
    db.commit()

