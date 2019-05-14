from flask import Flask
from forms import *
from flask import session, send_file
from flask import request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

import os
from database import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum58_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
@app.route('/index')
def index():
    return "Привет, Яндекс!"


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if not UserModel.user_exists(form.username.data):
            user = User(username=form.username.data,
                        password_hash=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()

            user = User.query.filter_by(username=form.username.data).first()
            session.clear()
            session['username'] = user.username
            session['user_id'] = user.id
            return redirect('/')

        form.submit.errors.append('Пользователь с таким именем уже зарегестрирован в системе. Исправьте данные')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            form.submit.errors.append('Такого пользователя нет в системе.')
        elif not check_password_hash(user.password_hash, form.password.data):
            form.submit.errors.append('Неправильный пароль')
        else:
            session.clear()
            session['username'] = user.username
            session['user_id'] = user.id
            return redirect('/')
    return render_template('login.html', title='Вход', form=form)


@app.route('/add-task', methods=['GET', 'POST'])
def add_task():
    form = AddTask()
    if form.validate_on_submit():
        # if User.query.filter_by(username=form.username.data).first() is None:
        #     user = User(username=form.username.data,
        #                 password_hash=generate_password_hash(form.password.data))
        #     db.session.add(user)
        #     db.session.commit()
        #
        #     user = User.query.filter_by(username=form.username.data).first()
        #     session.clear()
        #     session['username'] = user.username
        #     session['user_id'] = user.id
            return redirect('/')

        # form.submit.errors.append('Пользователь с таким именем уже зарегестрирован в системе. Исправьте данные')
    return render_template('add_task.html', title='Добавить таск', form=form)


@app.route('/users')
def users():
    return "Привет, Яндекс!"


@app.route('/task-categories')
def task_categories():
    return "Привет, Яндекс!"


@app.route('/admin')
def admin():
    return "Привет, Яндекс!"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
