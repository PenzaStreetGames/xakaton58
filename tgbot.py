from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from database import *


TOKEN = '846229948:AAGQ6Ey8qX_yRYFzrjVnWp7_dp9h68J7JhY'
updater = None
task_info = ["Название задачи", "Описание задачи", "Категория", "Дата завершения"]
current = 0
quest_mode = False


def main():
    global updater
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(text_handler)
    dp.add_handler(CommandHandler("auth", auth, pass_args=True, pass_user_data=True))
    dp.add_handler(CommandHandler("what", what, pass_user_data=True))
    dp.add_handler(CommandHandler("logout", logout, pass_user_data=True))
    dp.add_handler(CommandHandler("task", task))
    dp.add_handler(CommandHandler("expired_task", expired_task))
    dp.add_handler(CommandHandler("add_task", add_task))
    updater.start_polling()
    updater.idle()


def echo(bot, update):
    global current, quest_mode
    tg = Tg.query.filter_by(chat_id=get_chat_id(update)).first()
    if not quest_mode:
        return
    task_info[current] = update.message.text
    current += 1
    if current == 4:
        TaskModel.create(task_info[0], task_info[1], datetime.datetime.strptime(task_info[3], '%Y-%m-%d-%H.%M'),
                         User.query.filter_by(username=tg.login).first().id, category=task_info[2])
        update.message.reply_text("Добавлено")
        quest_mode = False
        return
    update.message.reply_text(task_info[current])


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


def add_task(bot, update):
    global quest_mode
    tg = Tg.query.filter_by(chat_id=get_chat_id(update)).first()
    if not tg:
        update.message.reply_text("Вы не авторизированы")
        return
    quest_mode = True
    update.message.reply_text(task_info[0])


# def valid_date(phrase):
#     if phrase.lower() == 'сегодня':
#

if __name__ == '__main__':
    main()