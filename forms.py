from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, \
    SelectField, DateTimeField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired


class LoginForm(FlaskForm):  # Форма входа
    username = StringField('Логин', validators=[
        DataRequired(message='Поле обязательно для заполнения'),
        Length(min=6, max=32, message='Логин должен быть длиной от 6 до 32 символов')])
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Поле обязательно для заполнения'),
        Length(min=8, max=32, message='Пароль должен быть длиной от 8 до 32 символов')])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):  # Форма регистрации
    username = StringField('Логин', validators=[
        DataRequired(message='Поле обязательно для заполнения'),
        Length(min=6, max=32, message='Логин должен быть длиной от 6 до 32 символов')])
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Поле обязательно для заполнения'),
        EqualTo('confirmation', message='Пароли должны совпадать'),
        Length(min=8, max=32, message='Пароль должен быть длиной от 8 до 32 символов')])
    confirmation = PasswordField('Подтвердите пароль', validators=[
        DataRequired(message='Поле обязательно для заполнения'),
        Length(min=8, max=32, message='Пароль должен быть длиной от 8 до 32 символов')])
    name = StringField('Имя', validators=[Length(max=80, message='Имя Не может быть длиннее 80')])
    surname = StringField('Фамилия', validators=[Length(max=80, message='Фамилия не может быть длиннее 80')])
    submit = SubmitField('Зарегистрироваться')


class AddTask(FlaskForm):  # Форма добавления задачи
    name = StringField('Название', validators=[
        DataRequired(message='Поле обязательно для заполнения'),
        Length(min=3, max=80, message='Название должено быть длиной от 3 до 80 символов')])
    desc = StringField('Описание', validators=[
        DataRequired(message='Поле обязательно для заполнения'),
        Length(min=3, max=1000, message='Описание должено быть длиной от 3 до 1000 символов')])

    date = DateTimeField()

    author = StringField('ФИО', validators=[
        DataRequired(message='Поле обязательно для заполнения'),
        Length(max=80, message='ФИО должно быть длиной до 80 символов')])

    submit = SubmitField('Добавить задачу')