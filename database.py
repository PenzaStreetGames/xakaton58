from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import time
from werkzeug.security import generate_password_hash


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

# Модели


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(160), nullable=False)
    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    banned = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'User ID{self.id}. {self.username}'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    priority = db.Column(db.Integer)
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    stage = db.Column(db.Integer)
    executed = db.Column(db.Boolean)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


class Stage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))


class Delegation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)


# Методы


class UserModel:

    @staticmethod
    def add_admin(username, password):
        if UserModel.user_exists(username):
            return

        admin = User(username=username,
                     password_hash=generate_password_hash(password),
                     is_admin=True)
        db.session.add(admin)
        db.session.commit()

    @staticmethod
    def find(id):
        user = User.query.filter(Task.author_id == id).all()
        if not user:
            return
        return user

    @staticmethod
    def add_user(username, password):
        if UserModel.user_exists(username):
            return

        user = User(username=username,
                    password_hash=generate_password_hash(password),
                    is_admin=False)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def is_admin(session):
        return 'user_id' in session and User.query.filter_by(
            User.id == session['user_id'], User.is_admin == True).first()

    @staticmethod
    def user_exists(username):
        return bool(User.query.filter_by(username=username).first())


class TaskModel:
    @staticmethod
    def get_comments(task_id):
        return Comment.query.filter_by(task_id=task_id).all()


    @staticmethod
    def create(name, description, date, author, executor=None, priority=1, category="",
               stage=1, tags=[]):
        task = Task(name=name,
                    description=description,
                    date=date,
                    author=author,
                    executor_id=executor,
                    priority=priority,
                    category=category,
                    stage=stage,
                    tags=tags)
        db.session.add(task)
        db.session.commit()

    @staticmethod
    def get_by_author(author):
        """получение задач пользователя"""
        task = Task.query.filter(Task.author_id == author).all()
        if not task:
            return []
        return task

    @staticmethod
    def is_delegated(task_id):
        return bool(Delegation.query.filter_by(task_id=task_id).count())

    @staticmethod
    def add_tags(task_id, tags):
        task = Task.query.filter_by(task_id=task_id).first()
        task.tags = f"{task.tags},{tags}"
        db.session.commit()

    @staticmethod
    def filter_by_tags(word, delegated_only=False):
        tasks = Task.query.filter_by(Task.tags.like(f"%{word}%")).all()
        if delegated_only:
            tasks = filter(lambda x: TaskModel.is_delegated(x.id), tasks)
        return tasks


class CategoryModel:

    @staticmethod
    def get_by_category(self, category):
        """получеие пользователя по id"""
        task = Task.query.filter(Task.id == category).all()
        if not task:
            return
        return task

    def delete(self):
        pass


class CommentModel:
    pass


db.create_all()
# UserModel.add_admin(*MAIN_ADMIN)
