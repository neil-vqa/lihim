import sqlite3
from .models import database, User, Group, Pair


def create():
    conn = sqlite3.connect("lihim/db/lihimdb.db")
    with database:
        database.create_tables([User, Group, Pair])