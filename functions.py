from dbhelper import *


# Проверка на админа
def is_admin(session):
    return 'user_id' in session and User.query.filter_by(User.id == session['user_id'], User.is_admin == True).first()


# Бан пользователя, его книг и лайков
# def ban_user(user_id):
#     if user_id == 1:
#         return 'Вы не можете забанить главного администратора'
#
#     moder = Moder.query.filter_by(user_id=user_id).first()
#     admin = Moder.query.filter_by(user_id=user_id).first()
#     user = User.query.filter_by(id=user_id).first()
#     books = Book.query.filter_by(uploader_id=user_id).all()
#     if moder:
#         db.session.delete(moder)
#     if admin:
#         db.session.delete(admin)
#
#     Like.query.filter_by(user_id=user_id).delete()
#     Comment.query.filter_by(user_id=user_id).delete()
#
#     for book in books:
#         Like.query.filter_by(book_id=book.id).delete()
#         Comment.query.filter_by(book_id=book.id).delete()
#         db.session.delete(book)
#         shutil.rmtree(f'static/books/{book.id}', ignore_errors=True)
#
#     db.session.delete(user)
#     db.session.commit()
#
#     return 'Пользователь успешно забанен'


def user_exists(username):
    return bool(User.query.filter_by(username=username).first())


def get_comments(task_id):
    return Comment.query.filter_by(task_id=task_id).all()
