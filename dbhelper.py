from constants import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(160), nullable=False)
    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    is_admin = db.Column(db.Boolean, nullable=False)
    banned = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'User ID{self.id}. {self.username}'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    date = db.Column(db.Time, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('tasks', lazy=True))
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
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))


db.create_all()