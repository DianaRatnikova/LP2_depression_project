import csv
from database.db import db_session
from database.models import Question


def save_questions_data(questions_list: list[dict]) -> None:
    print(f"{type(questions_list) = }")
# ВОПРОС: mypy выдаёт сообщение: Argument 1 to "bulk_insert_mappings" of "scoped_session" has incompatible type
# "type[Question]"; expected "Mapper[Any]"
# при обьявлении полей в БД, похоже, нужно делать аннотацю, я правильно понимаю? Как это сделать?
    db_session.bulk_insert_mappings(Question, questions_list)
    db_session.commit()


def read_csv(filename: str) -> None:
    fields = [
        'question', 
        'num_of_question_male', 
        'scale_d_n_yes_male',
        'scale_d_n_no_male',
        'scale_mdp_yes_male',
        'scale_mdp_no_male', 
        'num_of_question_female',
        'scale_d_n_yes_female',
        'scale_d_n_no_female', 
        'scale_mdp_yes_female',
        'scale_mdp_no_female'
        ]
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, fields, delimiter=';')
        questions_list = []
        for row in reader:
            questions_list.append(row)
        save_questions_data(questions_list)