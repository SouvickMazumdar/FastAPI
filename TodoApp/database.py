from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'
engine = create_engine(
	SQLALCHEMY_DATABASE_URL,
	connect_args={"check_same_thread": False}
)

"""
The 'connect_args' parameter is used to configure the database connection.
For SQLite, 'check_same_thread=False' allows the database connection to be shared across multiple threads.
This is necessary in FastAPI, where multiple threads may handle requests and interact with the database concurrently.
By default, SQLite restricts connections to a single thread, but FastAPI's async nature requires this flexibility.
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""
SessionLocal is a factory for creating new SQLAlchemy session objects.
Each session is bound to the engine defined above.
We set 'autocommit' and 'autoflush' to False to ensure full control over when changes are committed or flushed to the database.
Use SessionLocal() to get a session for interacting with the database in your API endpoints.
"""

Base = declarative_base()
"""
Base is the base class for all ORM models (database tables).
All SQLAlchemy models should inherit from Base.
This allows SQLAlchemy to keep track of models and create tables in the database as needed.
"""