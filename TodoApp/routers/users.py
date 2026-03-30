from fastapi import APIRouter, Depends, HTTPException, Path  # FastAPI framework and dependency injection

from sqlalchemy.orm import Session  # SQLAlchemy session for DB operations

from ..models import Todos, Users  # ORM model for todo items 

from typing import Annotated  # For advanced type hints

from ..database import SessionLocal  # DB engine and session factory
from starlette import status
from pydantic import BaseModel, Field
from passlib.context import CryptContext

from .auth import get_current_user


router = APIRouter(
    prefix='/user',
    tags=['user']

)  # Initialize FastAPI app
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

class Password(BaseModel):
    old_password: str
    new_pasword: str= Field(min_length=6)
    confirm_password: str

# class Phone_number(BaseModel):
#     phone_number: str



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


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status=401, detail='Authentication Failed')
    # print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    # print(user)
    user_detail=db.query(Users).filter(Users.id==user.get('id')).all()
    if user_detail is None:
        raise HTTPException(status=404, detail="User Not Found")
    return user_detail

@router.put("/change_password", status_code= status.HTTP_200_OK)
async def change_password(user: user_dependency, db: db_dependency, password: Password):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_row=db.query(Users).filter(Users.id==user.get('id')).first()
    if user_row is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not pwd_context.verify(password.old_password,user_row.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong old Password")
    if password.new_pasword!=password.confirm_password:
        raise HTTPException(status_code=404, detail="New pasword mismatched")
    user_row.hashed_password=pwd_context.hash(password.new_pasword)
    db.add(user_row)
    db.commit()
    db.refresh(user_row)
    return {"detail": "Password updated successfully"}


@router.put("/update_phone_number", status_code= status.HTTP_200_OK)

# async def update_phone_number(user: user_dependency, db: db_dependency, phone: Phone_number):
async def update_phone_number(user: user_dependency, db: db_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_row=db.query(Users).filter(Users.id==user.get('id')).first()
    if user_row is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_row.phone_number=phone_number
    db.add(user_row)
    db.commit()
    db.refresh(user_row)
    return {"detail": "Phone Number updated successfully"}

    
    
        
