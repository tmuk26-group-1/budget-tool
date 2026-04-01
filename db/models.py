from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    '''
    A class that represents the User table  
    ID, email, username must be unique  
    No fields left blank
    '''
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


