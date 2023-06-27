from database.models import User, Question, Answers
from database.db import db_session
from sqlalchemy import desc
import sqlalchemy
from constants import Gender


#def fname_query(fname: str)  -> sqlalchemy.orm.query.Query | None:
#    users_with_right_fname = User.query.filter(User.fname == fname)
#    return users_with_right_fname
#
#
#def lname_query(fname_query: sqlalchemy.orm.query.Query, lname: str)  -> sqlalchemy.orm.query.Query | None:
#    users_with_right_lname = fname_query.filter(fname_query.lname == lname)
#    return users_with_right_lname


def select_user_via_name(fname: str, lname: str)  -> sqlalchemy.orm.query.Query | None:
    user_to_find = User.query.filter(User.fname == fname, User.lname == lname).first()
    return user_to_find

def select_user_via_id(user_id: int)  -> sqlalchemy.orm.query.Query | None:
    user_to_find = User.query.filter(User.id == user_id).first()
    return user_to_find


def get_user_id(fname: str, lname: str)  -> int | None:
    user_to_find = select_user_via_name(fname, lname)
    if user_to_find:
# mypy ругается(        queries.py:30: error: "Query[Any]" has no attribute "id"  [attr-defined]
        user_id = user_to_find.id
        return user_id
    else:
        print(f"Пользователь {fname} {lname} не найден в БД")
        return None


def get_user_gender(user_id: int) -> Gender | None:
    user_to_find = select_user_via_id(user_id)
    if user_to_find:
        return user_to_find.gender
    else:
        print(f"Пользователь с id {user_id} не найден в БД")
        return None


def get_user_answers_from_database(user_id: int, user_gender: Gender) -> sqlalchemy.orm.query.Query:
    if (user_gender ==  Gender.FEMALE):
        user_answers = db_session.query(Answers, Question).filter(
                Question.id == Answers.question_id, 
                Question.num_of_question_female != 0
                ).order_by(Question.num_of_question_female)
    else:
        user_answers = db_session.query(Answers, Question).filter(
                Question.id == Answers.question_id, 
                Question.num_of_question_male != 0
                ).order_by(Question.num_of_question_male)
    return user_answers


def count_d_n_marks(user_answers: sqlalchemy.orm.query.Query, user_gender: Gender) -> int:
    d_n_marks = 0
    for answer, question in user_answers:
        if (user_gender ==  Gender.FEMALE):
            point_to_add = question.scale_d_n_yes_female if answer.answer == 1 else question.scale_d_n_no_female
            d_n_marks += point_to_add
        else:
            point_to_add = question.scale_d_n_yes_male if answer.answer == 1 else question.scale_d_n_no_male
            d_n_marks += point_to_add
    return d_n_marks


def count_mdp_marks(user_answers: sqlalchemy.orm.query.Query, user_gender: Gender) -> int:
    mdp_marks = 0
    for answer, question in user_answers:
        if (user_gender ==  Gender.FEMALE):
            point_to_add = question.scale_mdp_yes_female if answer.answer == 1 else question.scale_mdp_no_female
            mdp_marks += point_to_add
        else:
            point_to_add = question.scale_mdp_yes_male if answer.answer == 1 else question.scale_mdp_no_male
            mdp_marks += point_to_add
    return mdp_marks


if __name__ == '__main__':
    user_id = get_user_id('Diana', "Ratnikova")

# Несколько вопросов:
# 1. Всё равно где-то будет ветвление в зависимости от гендера, просто сейчас перенесла его в функции. Это норм?
# 2. Как было бы корректнее назвать функции, подсчитывающие оценки D-N и MDP? Я сама хз, что значал эти сокращения,
# поэтому выбрала названия функций count_d_n_marks, count_mdp_marks

    if user_id:
        user_gender = get_user_gender(user_id)
        if user_gender:
            user_answers = get_user_answers_from_database(user_id, user_gender)
            d_n_marks  =  count_d_n_marks(user_answers, user_gender)
            mdp_marks = count_mdp_marks(user_answers, user_gender)

            print(f"{d_n_marks = }, {mdp_marks = }")