#-*- coding:UTF-8 -*-

import os

DEBUG =True
SECRET_KEY=os.urandom(24)

HOSTNAME ='127.0.0.1'
PORT ='3306'
DATABASE='test'
USERNAME ='root'
PASSWORD ='123456'
SQLALCHEMY_DATABASE_URI='mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS =False

