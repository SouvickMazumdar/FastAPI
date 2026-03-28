

from fastapi import APIRouter, Depends, HTTPException, Path  # FastAPI framework and dependency injection

from sqlalchemy.orm import Session  # SQLAlchemy session for DB operations

from models import Todos  # ORM model for todo items

from typing import Annotated  # For advanced type hints

from database import SessionLocal  # DB engine and session factory
from starlette import status
from pydantic import BaseModel, Field


from .auth import get_current_user


router = APIRouter(
    prefix='/admin',
    tags=['admin']

)  # Initialize FastAPI app

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




@router.get("/todo",status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role')!='admin':
        raise HTTPException(status_code=401, detail="Authentication failed")
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db:db_dependency, todo_id: int= Path(gt=0)):
    if user is None:
        raise HTTPException(status=401, detail="Authentication Failed")
    todo_model=db.query(Todos).filter(Todos.id==todo_id).first()
    if todo_model is None:
        raise HTTPException(status=404, detail="Todo not found")
    db.query(Todos)\
    .filter(Todos.id==todo_id).delete()
    db.commit()

    