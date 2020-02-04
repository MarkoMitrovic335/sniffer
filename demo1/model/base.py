__all__ = ['engine', 'Base', 'Session']

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def db_create():
    engine = create_engine('sqlite:///./../model/demo2.db')
    return engine

# engine
engine = db_create()

# Base
Base = declarative_base()

# Session
Session = sessionmaker(bind=engine)
