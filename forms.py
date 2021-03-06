from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, \
    IntegerField, \
    SelectField, DateTimeField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired


class LoginForm(FlaskForm):  # Форма входа
    username = StringField('Логин', validators=[
        DataRequired(message='Поле обязательно для заполнения'),
        Length(min=5, max=32,
               message='Логин должен быть длиной от 6 до 32 символов')])
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Поле обязательно для заполнения'),
        Length(min=8, max=32,
               message='Пароль должен быть длиной от 8 до 32 символов')])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):  # Форма регистрации
    username = StringField('Логин', validators=[
        DataRequired(message='Поле обязательно для заполнения'),
        Length(min=6, max=32,
               message='Логин должен быть длиной от 6 до 32 символов')])
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Поле обязательно для заполнения'),
        EqualTo('confirmation', message='Пароли должны совпадать'),
        Length(min=8, max=32,
               message='Пароль должен быть длиной от 8 до 32 символов')])
    confirmation = PasswordField('Подтвердите пароль', validators=[
        DataRequired(message='Поле обязательно для заполнения'),
        Length(min=8, max=32,
               message='Пароль должен быть длиной от 8 до 32 символов')])
    name = StringField('Имя', validators=[
        Length(max=80, message='Имя Не может быть длиннее 80')])
    surname = StringField('Фамилия', validators=[
        Length(max=80, message='Фамилия не может быть длиннее 80')])
    submit = SubmitField('Зарегистрироваться')


class AddTask(FlaskForm):  # Форма добавления задачи
    name = StringField('Название', validators=[
        DataRequired(message='Поле обязательно для заполнения'),
        Length(min=3, max=80,
               message='Название должено быть длиной от 3 до 80 символов')])
    desc = StringField('Описание', validators=[
        DataRequired(message='Поле обязательно для заполнения'),
        Length(min=3, max=1000,
               message='Описание должено быть длиной от 3 до 1000 символов')])
    date = DateTimeField()
    submit = SubmitField('Добавить задачу')


class StatusForm(
    FlaskForm):  # Администраторская форма изменения статуса пользователей
    status_field = IntegerField('ID', validators=[
        DataRequired(message='Поле обязательно для заполнения')])
    status_select = SelectField(choices=[(a, a) for a in ['Участник', 'Админ']])
    status_submit = SubmitField('OK')


class BanForm(FlaskForm):  # Администраторская форма бана пользователей
    ban_field = IntegerField('ID',
                             validators=[DataRequired(
                                 message='Поле обязательно для заполнения')])
    ban_submit = SubmitField('OK')


class InfoForm(
    FlaskForm):  # Администраторская форма удобного получения информации о пользователе
    info_field = IntegerField('ID',
                              validators=[DataRequired(
                                  message='Поле обязательно для заполнения')])
    info_submit = SubmitField('OK')
