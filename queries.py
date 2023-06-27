from database.models import User, Question, Answers
from database.db import db_session
from sqlalchemy import desc
import sqlalchemy
from constants import Gender



def query_female_answers(user_id: int) -> sqlalchemy.orm.query.Query:
    # Вопрос. Окей, я отказалась от обратных слешей.
    # Каким образом теперь я могу сократить длину строк в запросе?
    # норм ли способ я использую (вынести условия фильтров в отдельные переменные)?
    filter_id = Question.id == Answers.question_id
    filter_num = Question.num_of_question_female != 0
    female_answers = db_session.query(Answers, Question).filter(filter_id, filter_num).order_by(Question.num_of_question_female)
    for answer, question in female_answers:
        print(f"{question.num_of_question_female}.){question.question}: {answer.answer}")
    return female_answers


def query_male_answers(user_id: int) -> sqlalchemy.orm.query.Query:
    filter_id = Question.id == Answers.question_id
    filter_num = Question.num_of_question_male != 0
    male_answers = db_session.query(Answers, Question).filter(filter_id, filter_num).order_by(Question.num_of_question_male)
    for answer, question in male_answers:
        print(f"{question.num_of_question_male}.){question.question}: {answer.answer}")
    return male_answers
    

def count_d_n_marks_female(female_answers: sqlalchemy.orm.query.Query) -> int:
    d_n_marks = 0
    for answer, question in female_answers:
        point_to_add = question.scale_d_n_yes_female if answer.answer == 1 else question.scale_d_n_no_female
        d_n_marks += point_to_add
    return d_n_marks


def count_mdp_marks_female(female_answers: sqlalchemy.orm.query.Query) -> int:
    mdp_marks = 0
    for answer, question in female_answers:
        point_to_add = question.scale_mdp_yes_female if answer.answer == 1 else question.scale_mdp_no_female
        mdp_marks += point_to_add
    return mdp_marks


def count_d_n_marks_male(male_answers: sqlalchemy.orm.query.Query) -> int:
    d_n_marks = 0
    for answer, question in male_answers:
        point_to_add = question.scale_d_n_yes_male if answer.answer == 1 else question.scale_d_n_no_male
        d_n_marks += point_to_add
    return d_n_marks


def count_mdp_marks_male(male_answers: sqlalchemy.orm.query.Query) -> int:
    mdp_marks = 0
    for answer, question in male_answers:
        point_to_add = question.scale_mdp_yes_male if answer.answer == 1 else question.scale_mdp_no_male
        mdp_marks += point_to_add
    return mdp_marks


def fname_query(fname: str)  -> sqlalchemy.orm.query.Query | None:
    users_with_right_fname = User.query.filter(User.fname == fname)
    return users_with_right_fname


def lname_query(fname_query: sqlalchemy.orm.query.Query, lname: str)  -> sqlalchemy.orm.query.Query | None:
    users_with_right_lname = fname_query.filter(fname_query.lname == lname)
    return users_with_right_lname


def select_user(fname: str, lname: str)  -> sqlalchemy.orm.query.Query | None:
    user_to_find = User.query.filter(User.fname == fname, User.lname == lname).first()
    return user_to_find


def get_user_id(fname: str, lname: str)  -> int | None:
    user_to_find = select_user(fname, lname)
    if user_to_find:
        return user_to_find.id
    else:
        print(f"Пользователь {fname} {lname} не найден в БД")


if __name__ == '__main__':
    user_id = get_user_id('Diana', "Ratn5ikova")
    if user_id:
        if (User.query.filter(User.id == user_id)[0].gender == Gender.FEMALE):
            user_answers = query_female_answers(user_id)
            d_n_marks  =  count_d_n_marks_female(user_answers)
            mdp_marks = count_mdp_marks_female(user_answers)
        elif (User.query.filter(User.id == user_id)[0].gender == Gender.MALE):
            user_answers = query_male_answers(user_id)
            d_n_marks  =  count_d_n_marks_male(user_answers)
            mdp_marks = count_mdp_marks_male(user_answers)
        print(f"{d_n_marks = }, {mdp_marks = }")