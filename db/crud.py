from .database import SessionLocal
from .models import User

def create_user(email, firstname, lastname, username, password):
    '''
    Method to create (add) a user to the DB
    '''
    session = SessionLocal()

    user = User(email=email, firstname=firstname, lastname=lastname, username=username, password=password)
    session.add(user)
    session.commit()

    session.close()


def get_users():
    '''
    Method that returns all rows from the user table
    '''
    session = SessionLocal()

    users = session.query(User).all()

    session.close()
    return users