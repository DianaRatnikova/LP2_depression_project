from sqlalchemy import Column, Integer, String, ForeignKey
from database.db import Base, engine
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    fname = Column(String)
    lname = Column(String)
    gender = Column(String(6))
    answers = relationship("Answers", back_populates="user")

    def __repr__(self):
        return f'<User {self.fname} {self.lname}, {self.gender}>'
    

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question = Column(String)
    num_of_question_male = Column(Integer)
    num_of_question_female = Column(Integer)
    answers = relationship("Answers", back_populates="question")

    def __repr__(self):
        return f"<Question {self.id}, {self.question}, {self.num_of_question_male}, {self.num_of_question_female}>"
    

class Answers(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), index=True, nullable=False)
    question_id = Column(Integer, ForeignKey(Question.id), index=True, nullable=False)
    answer = Column(Integer) # или Bool
    user = relationship("User", lazy='joined')
    question = relationship("Question", lazy='joined')

    def __repr__(self):
        return f"User: {self.user}; Question: {self.question}; Answer: {self.answer}"



