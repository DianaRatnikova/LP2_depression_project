from database.models import User, Question, Answers
from database.db import db_session
from sqlalchemy import desc
import sqlalchemy
from constants import Gender
from typing import  Any
from sqlalchemy.orm import load_only
from sqlalchemy.orm import Load


def select_user_via_name(fname: str, lname: str)  -> sqlalchemy.orm.query.Query | None:
    user_to_find = User.query.filter(User.fname == fname, User.lname == lname).first()
    return user_to_find

def select_user_via_id(user_id: int)  -> sqlalchemy.orm.query.Query | None:
    user_to_find = User.query.filter(User.id == user_id).first()
    return user_to_find


def get_user_id(user_to_find: sqlalchemy.orm.query.Query)  -> int:
    user_id = user_to_find.id  # type: ignore
    return user_id


def get_user_gender(user_id: int) -> Gender | None:
    user_to_find = select_user_via_id(user_id)
    if user_to_find:
        return user_to_find.gender  # type: ignore
    else:
        print(f"Пользователь с id {user_id} не найден в БД")
        return None


def count_mdp_marks1(user_answers: sqlalchemy.orm.query.Query, user_gender: Gender) -> int:
    mdp_marks = 0
    for answer, question in user_answers:
        if user_gender ==  Gender.FEMALE:
            point_to_add = question.scale_mdp_yes_female if answer.answer == 1 else question.scale_mdp_no_female
            mdp_marks += point_to_add
        else:
            point_to_add = question.scale_mdp_yes_male if answer.answer == 1 else question.scale_mdp_no_male
            mdp_marks += point_to_add
    return mdp_marks


def get_user_answers_from_database(user_id, num_of_question) -> sqlalchemy.orm.query.Query:
    user_answers = db_session.query(Answers, Question).filter(
                Question.id == Answers.question_id,
                Answers.user_id == user_id,
                num_of_question != 0
                ).order_by(num_of_question)
    return user_answers


if __name__ == '__main__':
    fname = 'Diana'
    lname = "Ratnikova"
    user_to_find = select_user_via_name(fname, lname)
    if user_to_find:
        user_id = get_user_id(user_to_find)
    else:
        print(f"Пользователь {fname} {lname} не найден в БД")

# Как могла избавилась от ветвления, но до сих пор уверенности нет
# С моей организацией БД не вижу варианта, когда по одной проверке гендера сразу бы назначались все гендерные переменные,
# тк в строке 73 сначала идёт обращение к Question, а все назначения переменных шкал возможны только после получения
# запроса user_answers. Блин, начинаю путаться и уже хз, как при данном раскладе перенести подсчёты d_n в функцию

    if user_id:
        user_gender = get_user_gender(user_id)
        if user_gender:
            num_of_question = Question.num_of_question_female if user_gender == Gender.FEMALE else Question.num_of_question_male
            user_answers = get_user_answers_from_database(user_id, num_of_question)

            d_n_marks = 0
            mdp_marks = 0

            for answer, question in user_answers:
                    scale_d_n_yes = question.scale_d_n_yes_female if user_gender == Gender.FEMALE else question.scale_d_n_yes_male
                    scale_d_n_no =  question.scale_d_n_no_female if user_gender == Gender.FEMALE else question.scale_d_n_no_male
                    d_n_marks += scale_d_n_yes if answer.answer == 1 else scale_d_n_no

                    scale_mdp_yes = question.scale_mdp_yes_female if user_gender == Gender.FEMALE else question.scale_mdp_yes_male
                    scale_mdp_no =  question.scale_mdp_no_female if user_gender == Gender.FEMALE else question.scale_mdp_no_male
                    mdp_marks += scale_mdp_yes if answer.answer == 1 else scale_mdp_no

            print(f"{d_n_marks = }, {mdp_marks = }")
