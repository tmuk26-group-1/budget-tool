from sqlalchemy.exc import IntegrityError
from sqlalchemy import extract
from .database import SessionLocal
from .models import User, Transaction, Category


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


def delete_user(email, password) -> tuple[bool, str]:
    '''
    Function to permanently delete a user from the database. Password required for safety.
    '''
    session = SessionLocal()

    try:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            return False, "No account with that email"
        
        if user.password != password:
            return False, "Wrong password"
        
        session.delete(user)
        
        session.commit()
        return True, "User deleted"
    
    except IntegrityError:
        session.rollback()
        return False, "Could not delete user"
    
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


def get_user_by_id(user_id):
    session = SessionLocal()
    try:
        return session.query(User).filter(User.user_id == user_id).first()
    finally:
        session.close()


def get_user_by_email(email):
    '''Fetch a single user by email'''
    session = SessionLocal()
    try:
        return session.query(User).filter(User.email == email).first()
    finally:
        session.close()



#function for updating your password
def update_password(email, new_password) -> tuple[bool, User | str]:
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.email == email).first()

        if not user:
            return False, "No account with that email"
        
        user.password = new_password
        session.commit()
        return True, user
    
    except Exception as e:
        session.rollback()
        return False, "Somthing, went wrong"
    
    finally:
        session.close()


def update_goal(email, amount) -> tuple[bool, User | str]:
    '''
    Update a single users monthly goal.\n
    If we want to remove the goal we can use None for the amount, as the field is nullable in the DB.
    '''
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.email == email).first()

        if not user:
            return False, "No account with that email"
        
        user.goal = amount
        session.commit()
        return True, user
    
    except IntegrityError as e:
        session.rollback()
        return False, "Could not update goal"   # fallback

    finally:
        session.close()


def create_transaction(user_id, amount, category_id, date, description = None) -> tuple[bool, Transaction | str]:
    session = SessionLocal()

    try:

        category = session.query(Category).filter(Category.category_id == category_id).first() 
        if not category:
            return False, "Category does not exist"
        
        transaction = Transaction(user_id=user_id, amount=amount, category_id=category_id, date=date, description=description)
        session.add(transaction)
        session.commit()
        return True, transaction
    
    except IntegrityError as e:
        session.rollback()
        return False, "Database constraint violation"   # fallback 

    finally:
        session.close()


def get_transaction(user_id, year, month):
    session = SessionLocal()
    try:
        return session.query(Transaction).filter(
            Transaction.user_id == user_id,
            extract("year", Transaction.date) == year,
            extract("month", Transaction.date) == month
        ).all()
    finally:
        session.close()


def create_category(name) -> tuple[bool, Category | str]:
    session = SessionLocal()

    try:
        cat = Category(name=name)
        session.add(cat)
        session.commit()
        return True, cat
    
    except IntegrityError as e:
        session.rollback()
        if "name" in str(e.orig):
            return False, "Category already exists"
        return False, "Database constraint violation"   # fallback 

    finally:
        session.close()


def get_category():
    session = SessionLocal()

    try:
        return session.query(Category).all()
    finally:
        session.close()

def pre_categories():
    categories = ["Salary", "Food & Groceries", "Rent & Housing", "Entertainment", "Other"]
    for name in categories:
        create_category(name)


def get_balance(user_id, year, month):
    session = SessionLocal()
    try:
        transactions = get_transaction(user_id, year, month)
        return sum(t.amount for t in transactions)
    finally:
        session.close()

def get_category_totals(user_id, year, month):
    session = SessionLocal()
    try:
        transactions = session.query(Transaction, Category).join(
            Category, Transaction.category_id == Category.category_id
        ).filter(
            Transaction.user_id == user_id,
            extract("year", Transaction.date) == year,
            extract("month", Transaction.date) == month
        ).all()

        totals = {}
        for t, cat in transactions:
            if cat.name not in totals:
                totals[cat.name] = 0
            totals[cat.name] += abs(t.amount)
        return totals
    finally:
        session.close()

def get_total_savings(user_id):
    session = SessionLocal()
    try:
        transactions = session.query(Transaction).filter(Transaction.user_id == user_id, Transaction.amount > 0).all()
        return sum(t.amount for t in transactions)
    finally:
        session.close()


def add_income(user_id, amount, category_id, date, description = None):
    return create_transaction(user_id, abs(amount), category_id, date, description)


def add_expense(user_id, amount, category_id, date, description=None):
    return create_transaction(user_id, -abs(amount), category_id, date, description)