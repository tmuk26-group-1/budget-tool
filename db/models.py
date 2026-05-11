from sqlalchemy import Column, Integer, String, ForeignKey, Date 
from .database import Base

class User(Base):
    '''
    A class that represents the User table  
    ID, email, username must be unique  
    No fields left blank
    '''
    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    goal = Column(Integer, nullable=True)
    savings = Column (Integer, default=0)

class Transaction(Base): 
    __tablename__ = "Transactions"

    transaction_id = Column(Integer, primary_key=True) 
    user_id = Column(Integer, ForeignKey("Users.user_id"), nullable = False)
    amount = Column(Integer, nullable = False)
    category_id = Column(Integer, ForeignKey("Categories.category_id"), nullable=False)
    date = Column(Date, nullable = False)
    description = Column(String)


class Category(Base):

    __tablename__ = "Categories"

    category_id = Column(Integer, primary_key = True)
    name = Column(String, unique = True, nullable = False)
    