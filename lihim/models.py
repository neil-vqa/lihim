from re import U
import sqlite3
from peewee import SqliteDatabase, Model, CharField, ForeignKeyField, BlobField
from .config import ConfigPath
import nacl.secret
import nacl.utils


conf = ConfigPath()

database = SqliteDatabase(conf.db_path)

class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()

class Group(BaseModel):
    name = CharField()
    user = ForeignKeyField(User, backref='groups')

class Pair(BaseModel):
    key_string = CharField()
    value_string = BlobField()
    group = ForeignKeyField(Group, backref='pairs')
    user = ForeignKeyField(User, backref='pairs')

def create_db():
    conf.create_config()
    conn = sqlite3.connect(conf.db_path)
    conn.close()

    with database:
        database.create_tables([User, Group, Pair])

def check_user_exists(username: str):
    try:
        User.get(User.username==username)
        return True
    except User.DoesNotExist:
        return False
    except Exception as e:
        raise e

def create_key(key_path: str, key_name: str, username: str):
    try:
        check = check_user_exists(username)
        if check == False:
            key_file = f"{key_path}/{key_name}"

            with open(key_file, "wb") as f:
                key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
                f.write(key)

            return key_file
        else:
            raise ValueError(f"User {username} already exists.")
    except Exception as e:
        raise e
