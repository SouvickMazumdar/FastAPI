
"""
models.py

This file defines the SQLAlchemy ORM model for the 'todos' table used in the FastAPI Todo application.
It imports the necessary base class and column types, and creates the Todos class which maps to the database table.
"""

from database import Base  # Import the SQLAlchemy Base class from the database module
from sqlalchemy import Column, Integer, String, Boolean  # Import column types from SQLAlchemy

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

