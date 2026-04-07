from sqlalchemy.exc import IntegrityError
from .database import SessionLocal
from .models import User

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