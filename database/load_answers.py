import csv
from database.models import Answers
from database.db import db_session
from sqlalchemy.exc import SQLAlchemyError
from database.load_questions import save_questions_data

def create_answer(row):
    answer = Answers(
        user_id = row['user_id'],
        question_id = row['question_id'],
        answer = row['answer']
    )
    db_session.add(answer)
    try:
        db_session.commit()
    except SQLAlchemyError:
        db_session.rollback()
        raise

def prepare_data(row):
    row['user_id'] = int(row['user_id'])
    row['question_id'] = int(row['question_id'])
    row['answer'] = str(row['answer'])
    return row


def process_row(row):
    row = prepare_data(row)
    create_answer(row)


def print_error(row_num, error_text, exception):
    print(f"Ошибка на строке {row_num}")
    print(error_text.format(exception))
    print('-' * 100)


def read_answers_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['user_id', 'question_id', 'answer']
        reader = csv.DictReader(f, fields, delimiter=';')
        for row_num, row in enumerate(reader, start=1):
            try:
                process_row(row)
            except (TypeError, ValueError) as e:
                print_error(row_num, "Неправильный формат данных {}", e)
            except SQLAlchemyError as e:
                print_error(row_num, "Ошибка целостности данных {}", e)
