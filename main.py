
from database.db import Base, engine
from database.add_user import add_user
from database.load_questions import read_csv
from database.create_answers import fake_answers_list, generate_data
from database.load_answers import read_answers_csv
import time

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    add_user()
    start = time.time()
    read_csv('questions.csv')
    print('Данные загружены за ', time.time() - start)
    generate_data(fake_answers_list(), 'answers.csv')
    read_answers_csv('answers.csv')