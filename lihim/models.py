from peewee import SqliteDatabase, Model, CharField, ForeignKeyField

DATABASE = "lihim/db/lihimdb.db"

database = SqliteDatabase(DATABASE)

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
    value_string = CharField(max_length=512)
    group = ForeignKeyField(Group, backref='pairs')

