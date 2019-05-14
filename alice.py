from flask import Flask, request
import logging
import json
from database import *
from werkzeug.security import check_password_hash, generate_password_hash
"""https://Wignorbo.pythonanywhere.com/post"""

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
sessionStorage = {}


@app.route("/post", methods=["POST"])
def main():
    data = request.json
    logging.info(f"Request: {data}")
    response = {
        "session": data["session"],
        "version": data["version"],
        "response": {
            "end_session": False
        }
    }
    handle_dialog(data, response)
    logging.info(f"Response: {response}")

    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req["session"]["user_id"]
    if req["session"]["new"]:
        sessionStorage[user_id] = {
            "username": False,
            "password": False
        }
        res["response"]["text"] = "Привет, введи имя!"
        return
    if not sessionStorage[user_id]["username"]:
        username = req["request"]["original_utterance"]
        auth = UserModel.user_exists(username)
        if not auth:
            res["response"]["text"] = "Такого пользователя нет. Введи ещё раз."
            return
        sessionStorage[user_id]["username"] = username
        res["response"]["text"] = "Введи пароль."
        return
    if not sessionStorage[user_id]["password"]:
        password = req["request"]["original_utterance"]
        auth = UserModel.user_with_password(sessionStorage[user_id]["username"],
                                            password)
        if auth == "no password":
            res["response"]["text"] = "Неправильный пароль. Введи ещё раз."
            return
        sessionStorage[user_id]["password"] = password
        res["response"]["text"] = f"{sessionStorage[user_id]['username']}, " \
            f"вы авторизовались"
        return
    res["response"]["text"] = "Вы авторизованы. И всё."
