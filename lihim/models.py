import os
import sqlite3
from peewee import SqliteDatabase, Model, CharField, ForeignKeyField, BlobField
from .config import ConfigPath


conf = ConfigPath()

database = SqliteDatabase(conf.db_path)

class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    box_key = BlobField()

class Group(BaseModel):
    name = CharField()
    user = ForeignKeyField(User, backref='groups')

class Pair(BaseModel):
    key_string = CharField()
    value_string = CharField(max_length=512)
    group = ForeignKeyField(Group, backref='pairs')
    user = ForeignKeyField(User, backref='pairs')

def create_db():
    conf.create_config()
    conn = sqlite3.connect(conf.db_path)
    conn.close()

    with database:
        database.create_tables([User, Group, Pair])
