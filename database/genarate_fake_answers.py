import csv
import random
from database.models import User, Question, Answers
from database.db import db_session
from sqlalchemy.exc import SQLAlchemyError


def fake_answers_list() -> list[list[str]]:
    answers_list = []
    users = User.query.all()
    questions = Question.query.all()
    for user in users:
        for question in questions:
            answer = [user.id, question.id, random.choice([0, 1])]
            answers_list.append(answer)
    return answers_list


def create_answer(string_for_db:  dict) -> None:
    answer = Answers(
        user_id = string_for_db['user_id'],
        question_id = string_for_db['question_id'],
        answer = string_for_db['answer']
    )
    db_session.add(answer)
    db_session.commit()


def prepare_data(row: list[str]) -> dict:
    string_for_db = {
        'user_id': int(row[0]),
        'question_id': int(row[1]),
        'answer': int(row[2])
        }
    return string_for_db


def process_row(row: list) -> None:
    string_for_db = prepare_data(row)
    create_answer(string_for_db)


def print_error(row_num: int, error_text: str, exception: TypeError | ValueError| SQLAlchemyError) -> None:
    print(f"Ошибка на строке {row_num}")
    print(error_text.format(exception))
    print('-' * 100)


def add_fake_answers_to_db(data_list: list[list[str]]) -> None:
    for row_num, row in enumerate(data_list):
        try:
            process_row(row)
        except (TypeError, ValueError) as e:
            print_error(row_num, "Неправильный формат данных {}", e)
        except SQLAlchemyError as e:
           print_error(row_num, "Ошибка целостности данных {}", e)

