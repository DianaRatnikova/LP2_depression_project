import csv
import random

from database.models import User, Question


def fake_answers_list():
    data = []
    users = User.query.all()
    questions = Question.query.all()
    for user in users:
        for question in questions:
            answer = [user.id, question.id, random.choice([0, 1])]
            data.append(answer)
    return data


def generate_data(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        for row in data:
            writer.writerow(row)


    generate_data(fake_answers_list(), 'answers.csv')