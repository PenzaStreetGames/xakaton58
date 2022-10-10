from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from database import *


TOKEN = 'aboba'
updater = None


def main():
    global updater
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, echo, pass_user_data=True)
    dp.add_handler(text_handler)
    dp.add_handler(CommandHandler("auth", auth, pass_args=True, pass_user_data=True))
    dp.add_handler(CommandHandler("what", what, pass_user_data=True))
    dp.add_handler(CommandHandler("logout", logout, pass_user_data=True))
    dp.add_handler(CommandHandler("task", task))
    dp.add_handler(CommandHandler("expired_task", expired_task))
    dp.add_handler(CommandHandler("add_task", add_task, pass_user_data=True))
    updater.start_polling()
    updater.idle()


def echo(bot, update, user_data):
    tg = Tg.query.filter_by(chat_id=get_chat_id(update)).first()
    if not user_data['quest_mode']:
        return
    user_data['task_info'][user_data['current']] = update.message.text
    user_data['current'] += 1
    if user_data['current'] == 4:
        corrected, date = valid_date(user_data['task_info'][3])
        if not corrected:
            date = datetime.datetime.strptime(date, '%Y-%m-%d-%H.%M')
        TaskModel.create(user_data['task_info'][0], user_data['task_info'][1], date,
                         User.query.filter_by(username=tg.login).first().id, category=user_data['task_info'][2])
        update.message.reply_text("Добавлено")
        user_data['quest_mode'] = False
        return
    update.message.reply_text(user_data['task_info'][user_data['current']])


def auth(bot, update, args, user_data):
    tg = Tg.query.filter_by(chat_id=get_chat_id(update)).first()
    if tg:
        update.message.reply_text("Вы уже вошли")
        return
    login, pswd = args
    if not UserModel.user_exists(login):
        update.message.reply_text("Нет такого пользователя")
    else:
        user = User.query.filter_by(username=login).first()
        if not check_password_hash(user.password_hash, pswd):
            update.message.reply_text("Неправильный пароль")
        else:
            update.message.reply_text(f"Привет,  {user.username}")
            user_data['login'] = login
            db.session.add(Tg(login=login, chat_id=get_chat_id(update)))
            db.session.commit()


def what(bot, update, user_data):
    tg = Tg.query.filter_by(chat_id=get_chat_id(update)).first()
    if not tg:
        update.message.reply_text("Вы не авторизированы")
        return
    update.message.reply_text(tg.login)


def logout(bot, update, user_data):
    tg = Tg.query.filter_by(chat_id=get_chat_id(update)).first()
    if tg:
        db.session.delete(tg)
        db.session.commit()
    update.message.reply_text("Успешно вышли")


def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id


def task(bot, update):
    tg = Tg.query.filter_by(chat_id=get_chat_id(update)).first()
    if not tg:
        update.message.reply_text("Вы не авторизированы")
        return
    result = ""
    tasks = Task.query.filter_by(author_id=User.query.filter_by(username=tg.login).first().id).all()
    for t in tasks:
        result += f"ID{t.id}. {t.name} - {t.date.strftime('%Y-%m-%d-%H.%M')}\n"

    update.message.reply_text(result)


def expired_task(bot, update):
    tg = Tg.query.filter_by(chat_id=get_chat_id(update)).first()
    if not tg:
        update.message.reply_text("Вы не авторизированы")
        return
    result = ""
    tasks = Task.query.filter_by(author_id=User.query.filter_by(username=tg.login).first().id).all()
    for t in tasks:
        if t.date > datetime.datetime.now():
            continue
        result += f"ID{t.id}. {t.name} - {t.date.strftime('%Y-%m-%d-%H.%M')}\n"

    update.message.reply_text(result)


def add_task(bot, update, user_data):
    tg = Tg.query.filter_by(chat_id=get_chat_id(update)).first()
    if not tg:
        update.message.reply_text("Вы не авторизированы")
        return
    user_data['quest_mode'] = True
    user_data['current'] = 0
    user_data['task_info'] = ["Название задачи", "Описание задачи", "Категория", "Дата завершения"]
    update.message.reply_text(user_data['task_info'][0])


def valid_date(phrase):
    if phrase.lower() == 'сегодня':
        return True, datetime.datetime.today()
    elif phrase.lower() == 'завтра':
        return True, datetime.datetime.now() + datetime.timedelta(days=1)
    elif phrase.lower() == 'послезавтра':
        return True, datetime.datetime.now() + datetime.timedelta(days=2)
    else:
        weekdays = 'понедельник вторник сред четверг пятниц суббот воксресен'.split()
        for i in range(7):
            if weekdays[i] in phrase.lower():
                days = (i-datetime.datetime.now().weekday()) % 7
                if datetime.datetime.now().weekday() == i:
                    days += 7
                return True, datetime.datetime.now() + \
                       datetime.timedelta(days=days)
        return False, phrase


if __name__ == '__main__':
    main()
