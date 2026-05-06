from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
# from .database import engine, Base
# from .models import User

DATABASE_URL = "sqlite:///db/budget.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def init_db():
    '''
    Function to initialize database
    Adds all missing tables.
    '''
    Base.metadata.create_all(engine)
    from db.crud import pre_categories
    pre_categories()
