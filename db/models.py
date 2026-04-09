from sqlalchemy import Column, Integer, String, ForeignKey, Date 
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


class transactions(Base):
    __tablename__ = "Transactions"

    transaction_id = Column(Integer, primary_key=True) 
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable = False)
    amount = Column(Integer, nullable = False)
    category_name = Column(String, nullable = False)
    date = Column(Date, nullable = False)
    description = Column(String)


class category(Base):

    __tablename__ = "Category"

    category_id = Column(Integer, primary_key = True)
    name = Column(String, unique = True, nullable = False)
    