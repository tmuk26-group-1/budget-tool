from sqlalchemy.exc import IntegrityError
from .database import SessionLocal
from .models import User, transactions, category

def create_user(email, firstname, lastname, username, password) -> tuple[bool, User | str]:
    '''
    Method to create (add) a user to the DB.  
    Returns (True, user) on success, or (False, error_message) on failure.
    '''
    session = SessionLocal()

    try:
        user = User(email=email, firstname=firstname, lastname=lastname, username=username, password=password)
        session.add(user)
        session.commit()
        return True, user

    except IntegrityError as e:
        session.rollback()
        if "email" in str(e.orig):
            return False, "Email already registered"
        if "username" in str(e.orig):
            return False, "Username already taken"
        return False, "Database constraint violation"   # fallback 

    finally:
        session.close()


def get_users():
    '''
    Method that returns all rows from the user table
    '''
    session = SessionLocal()
    try:
        return session.query(User).all()
    finally:
        session.close()


def create_transaction(user_id, amount, category_name, date, description = None):
    session = SessionLocal()

    transaction = transactions(user_id=user_id, amount=amount, category_name=category_name, date=date, description=description)
    session.add(transaction)
    session.commit()
    session.close()

def get_transaction(user_id):
    session = SessionLocal()

    trans = session.query(transactions).filter(transactions.user_id == user_id).all()
    session.close()
    return trans

def create_category(name):
    session = SessionLocal()

    cat = category(name=name)
    session.add(cat)
    session.commit()
    session.close()

def get_category():
    session = SessionLocal()

    cat = session.query(category).all()
    session.close()
    return cat



    
    
