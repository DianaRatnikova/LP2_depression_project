from database.models import User, Question, Answers
from database.db import db_session
from sqlalchemy import desc
from constants import Gender

# Написала отдельные функции - заготовки с запросами и подсчётом оценок.
# Вопрос: коректный ли у них вид, 
# норм ли логика разделения на м и ж, 
# норм ли считаются баллы,
# или посоветуешь усложнить запросы и высчитывать сумму средствами sql?


def show_female_answers(user_id):
    female_answers = db_session.query(Answers, Question).\
    filter(Question.id == Answers.question_id).\
    filter(Question.num_of_question_female != 0).\
    order_by(Question.num_of_question_female)
    for answer, question in female_answers:
        print(f"{question.num_of_question_female}.){question.question}: {answer.answer}")


def show_male_answers(user_id):
    male_answers = db_session.query(Answers, Question).\
    filter(Question.id == Answers.question_id).\
    filter(Question.num_of_question_male != 0).\
    order_by(Question.num_of_question_male)
    for answer, question in male_answers:
        print(f"{question.num_of_question_male}.){question.question}: {answer.answer}")


def count_female_marks(user_id):
    d_n_marks = 0
    mdp_marks = 0
    female_answers = db_session.query(Answers, Question).\
    filter(Question.id == Answers.question_id).\
    filter(Question.num_of_question_female != 0).\
    order_by(Question.num_of_question_female)

    for answer, question in female_answers:
        if answer.answer == 1:
            d_n_marks += question.scale_d_n_yes_female
            mdp_marks += question.scale_mdp_yes_female
        if answer.answer == 0:
            d_n_marks += question.scale_d_n_no_female
            mdp_marks += question.scale_mdp_no_female
    return d_n_marks, mdp_marks
    

if __name__ == '__main__':
    user_id = 1
    if (User.query.filter(User.id == user_id)[0].gender == Gender.FEMALE):
        show_female_answers(user_id)
        d_n_marks, mdp_marks =  count_female_marks(user_id)
        print(f"{d_n_marks = }, {mdp_marks = }")
    elif (User.query.filter(User.id == user_id)[0].gender == Gender.MALE):
        show_male_answers(user_id)
