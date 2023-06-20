import constants
from database.db import db_session
from database.models import User

def add_user():
    first_user = User(fname='Diana', lname = "Ratnikova", gender = constants.gender_female)
    db_session.add(first_user)
    db_session.commit()