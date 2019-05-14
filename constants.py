from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

DATABASE_NAME = "database.db"
TITLE = "TaskDelegator"
STATUSES = {
    'user': 'Пользователь',
    'admin': 'Администратор'
}
MAIN_ADMIN = ('admin', 'password')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum58_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)