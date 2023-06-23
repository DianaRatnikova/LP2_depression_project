from constants import Gender
from database.db import db_session
from database.models import User

def add_user() -> None:
    first_user = User(fname='Diana', lname = "Ratnikova", gender = Gender.FEMALE)
    db_session.add(first_user)
    db_session.commit()
    print(f"{type(Gender.FEMALE) = }")