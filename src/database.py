from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://admin:admin@localhost/tg_game')
Base = declarative_base()

def get_session():
    Session = sessionmaker(bind=engine)
    return Session()

def get_base():
    return Base

def create_all_tables(base):
    Base.metadata.create_all(engine)