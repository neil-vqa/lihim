import sqlite3
import json

from peewee import EnclosedNodeList
from .models import database, User, Group, Pair


def create_db():
    conn = sqlite3.connect("lihim/db/lihimdb.db")
    conn.close()

    with database:
        database.create_tables([User, Group, Pair])

def checker():
    return database

def create_user(username: str, password: str) -> None:
    new_user = User(username=username, password=password)
    new_user.save()

def check_users():
    users = User.select()
    return users
    
def enter_user(username: str, password: str):
    auth = {
        "LIHIM_USER": username,
        "LIHIM_PASSWORD": password
    }
    auth_dump = json.dumps(auth, indent=2)

    with open("lihim/db/session.json", "w") as f:
        f.write(auth_dump)

    try:
        allow_user()
    except Exception as e:
        raise e

def load_session_json():
    with open("lihim/db/session.json", "r") as f:
        current_user = json.load(f)

    username = current_user['LIHIM_USER']
    password = current_user['LIHIM_PASSWORD']

    return username, password

def get_user(username):
    try:
        user = User.get(User.username==username)
        return user
    except:
        raise ValueError("User does not exist.")

def check_password(current_user, password):
    if current_user.password == password:
        return True
    else:
        raise ValueError("Incorrect password.")

def allow_user():
    username, password = load_session_json()

    try:
        current_user = get_user(username)
        check_password(current_user, password)
        return True
    except Exception as e:
        raise e

def clear_user():
    auth = {
        "LIHIM_USER": "",
        "LIHIM_PASSWORD": ""
    }
    auth_dump = json.dumps(auth, indent=2)

    with open("lihim/db/session.json", "w") as f:
        f.write(auth_dump)

