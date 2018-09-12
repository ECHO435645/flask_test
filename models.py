#-*- coding:UTF-8 -*-
from werkzeug.security import generate_password_hash,check_password_hash
from exts import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.INTEGER,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(16),nullable=False)

    # def __init__(self,*args,**kwargs):
    #     telephone = kwargs.get('telephone')
    #     username = kwargs.get('username')
    #     password = kwargs.get('password')
    #
    #     telephone = self.telephone
    #     username = self.username
    #     password = generate_password_hash(password)
    # def check_password(self,raw_password):
    #     result = check_password_hash(self.password,raw_password)
    #     return result

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.INTEGER,primary_key=True,autoincrement=True)
    title = db.Column(db.String(50),nullable=False)
    content = db.Column(db.String(200),nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now())
    author_id = db.Column(db.INTEGER,db.ForeignKey('user.id'))
    author = db.relationship('User',backref = db.backref('questions'))

class Comment(db.Model):
    __tablename__ = 'comment'
    id= db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    content = db.Column(db.String(200),nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    question_id = db.Column(db.INTEGER,db.ForeignKey('questions.id'))
    author_id = db.Column(db.INTEGER,db.ForeignKey('user.id'))

    question = db.relationship('Question',backref = db.backref('comments',order_by = create_time.desc()))
    author = db.relationship('User', backref=db.backref('comments'))