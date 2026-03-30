
"""
models.py

This file defines the SQLAlchemy ORM model for the 'todos' table used in the FastAPI Todo application.
It imports the necessary base class and column types, and creates the Todos class which maps to the database table.
"""

from .database import Base  # Import the SQLAlchemy Base class from the database module
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey  # Import column types from SQLAlchemy


class Users(Base):
    __tablename__='users'
    id=Column(Integer, primary_key=True, index=True)
    email= Column(String, unique=True)
    username= Column(String, unique=True)
    first_name= Column(String)
    last_name= Column(String)
    hashed_password= Column(String)
    is_active= Column(Boolean, default=True)
    role= Column(String)
    phone_number=Column(String)


class Todos(Base):
    """
    ORM model for the 'todos' table.
    Each instance of this class represents a row in the 'todos' table.
    """
    __tablename__ = 'todos'  # Name of the table in the database
    id = Column(Integer, primary_key=True, index=True)  # Unique ID for each todo, primary key, indexed for fast lookup
    title = Column(String)  # Title of the todo item
    description = Column(String)  # Detailed description of the todo item
    priority = Column(Integer)  # Priority level of the todo item
    complete = Column(Boolean, default=False)  # Completion status, defaults to False
    owner_id=Column(Integer, ForeignKey(Users.id))

