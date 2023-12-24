from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship

engine = create_engine('postgresql://admin:admin@localhost/tg_game')

class Base(DeclarativeBase): pass

Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    """
    Сreating a users table in the database
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(Integer)
    score = Column(Integer)
    penalties = Column(Integer)
    rating = Column(Integer)
    clan_id = Column(Integer, ForeignKey("clans.id"))
    clan = relationship("Clan", back_populates="users")

class Clan(Base):
    """
    Сreating a clans table in the database
    """

    __tablename__ = "clans"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    chat_id = Column(Integer)
    users = relationship("User", back_populates="clan")
    wins = Column(Integer)
    losses = Column(Integer)
    rating = Column(Integer)

def create_all_tables():
    """
    Creates all tables defined in models
    """

    Base.metadata.create_all(engine)