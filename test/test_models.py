import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date


from db.database import Base
from db.models import User, Transaction, Category


engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

@pytest.fixture
def db_session():
    """Skapar tabeller och en session för varje test."""
    Base.metadata.create_all(engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

# --- TESTS --- #

def test_user_model_creation(db_session):
    """Testar att User-modellen sparar data korrekt."""
    new_user = User(
        email="model@test.com",
        firstname="Kalle",
        lastname="Anka",
        username="kalle_anka",
        password="password123"
    )
    db_session.add(new_user)
    db_session.commit()

    user = db_session.query(User).filter_by(username="kalle_anka").first()
    assert user is not None
    assert user.firstname == "Kalle"
    assert user.email == "model@test.com"

def test_category_and_transaction_relationship(db_session):
    """Testar att transaktioner kan kopplas till kategorier."""

    food_cat = Category(name="Mat")
    db_session.add(food_cat)
    db_session.commit()

    new_trans = Transaction(
        user_id=1,  
        amount=200,
        category_id=food_cat.category_id,
        date=date(2026, 4, 17),
        description="ICA handling"
    )
    db_session.add(new_trans)
    db_session.commit()

    
    saved_trans = db_session.query(Transaction).first()
    assert saved_trans.amount == 200
    assert saved_trans.category_id == food_cat.category_id

def test_user_nullable_constraints(db_session):
    """Testar att databasen kastar fel om obligatoriska fält saknas."""
    from sqlalchemy.exc import IntegrityError
    
    broken_user = User(firstname="Fel", lastname="Namn", username="noemail", password="123")
    db_session.add(broken_user)
    
    with pytest.raises(IntegrityError):
        db_session.commit()