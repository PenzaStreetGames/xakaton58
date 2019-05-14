from flask import Flask
from forms import *
from flask import session, send_file
from flask import request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

import os
from database import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum58_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
stages = {
    1: "Новая",
    2: "Начата",
    3: "Закончена"
}


@app.route('/')
@app.route('/index')
def index():
    is_login = session.get("user_id", None)
    if is_login:
        tasks = TaskModel.get_by_author(session["user_id"])
    else:
        tasks = []
    params = {
        "is_login": is_login,
        "tasks": tasks,
        "task_number": len(tasks)
    }
    return render_template("index.html", **params)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if not UserModel.user_exists(form.username.data):
            user = User(username=form.username.data,
                        password_hash=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()

            return redirect('/success')
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


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/add-task', methods=['GET', 'POST'])
def add_task():
    if 'username' not in session:
        return redirect('/login')

    form = AddTask()
    if form.validate_on_submit():
        TaskModel.create(form.name.data, form.desc.data, session['user_id'], form.date.data)
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


@app.route("/task_edit/<int:task_id>")
def task_edit(task_id):
    return "Редактирование"


@app.route("/task_info/<int:task_id>")
def task_info(task_id):
    return "Информация"


@app.route("/task_delete/<int:task_id>")
def task_delete(task_id):
    return "Удаление"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
