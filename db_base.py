from constants import *
from dbhelper import *
import functions

from werkzeug.security import generate_password_hash


def add_admin(username, password):
    if functions.user_exists(username):
        return

    admin = User(username=username,
                 password_hash=generate_password_hash(password),
                 is_admin=True)
    db.session.add(admin)
    db.session.commit()


def add_user(username, password):
    if functions.user_exists(username):
        return

    user = User(username=username,
                password_hash=generate_password_hash(password),
                is_admin=False)
    db.session.add(user)
    db.session.commit()


add_admin(*MAIN_ADMIN)