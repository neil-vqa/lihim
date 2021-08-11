from typing import List
import typer
from .models import create_db
from .db import *


app = typer.Typer()

@app.command()
def initdb():
    """
    One-off command to create the database and tables.
    """
    create_db()
    typer.echo("Database created.")

@app.command()
def check():
    """
    Check who is currently logged in.
    """
    user = load_session_json()
    typer.echo(f"Current user: {user[0]}")

@app.command()
def useradd(username: str):
    """
    'useradd [username]' - Add a new user.
    """
    passwordx = typer.prompt("Password", hide_input=True)
    passwordy = typer.prompt("Retype password", hide_input=True)

    if passwordx == passwordy:
        try:
            create_user(username, passwordx)
            typer.echo(f"User {username} created.")
        except Exception as e:
            typer.echo(f"User {username} already exists.")
    else:
        typer.echo("Password did not match. Please try again.")

@app.command()
def users():
    """
    Lists all the users.
    """
    users_list = check_users()
    for user in users_list:
        typer.echo(user.username)

@app.command()
def login(
    username: str, 
    password: str = typer.Option(
        ..., prompt=True, hide_input=True
    )
):
    """
    'login [username]' - Login as a certain user.
    """
    try:
        enter_user(username, password)
        typer.echo(f"Logged in.")
    except Exception as e:
        typer.echo(e)

@app.command()
def logout():
    """
    Logout current user.
    """
    clear_user()
    typer.echo(f"Logged out. Bye!")

@app.command()
def groupadd(name: str):
    """
    'groupadd [group name]' - Add a new group.
    """
    try:
        allow_user()
        create_group(name)
        typer.echo(f"{name} group added.")
    except Exception as e:
        typer.echo(e)

@app.command()
def groups():
    """
    Lists all the groups of current user.
    """
    groups_list = check_groups()
    for group in groups_list:
        typer.echo(group.name)

@app.command()
def group(name: str):
    """
    'group [group name]' - Lists all the keys of the group.
    """
    pairs_list = check_group_pairs(name)
    for pair in pairs_list:
        typer.echo(pair.key_string)

@app.command()
def pairadd():
    """
    Add a new key-value pair.
    """
    key = typer.prompt("Key")
    value = typer.prompt("Value")
    group = typer.prompt("Add to what group?")

    try:
        allow_user()
        create_pair(key, value, group)
        typer.echo(f"{key} added.")
    except Exception as e:
        typer.echo(e)

@app.command()
def pairs():
    """
    Lists all the keys of available pairs of current user.
    """
    pairs_list = check_pairs()
    for pair in pairs_list:
        typer.echo(pair.key_string)

@app.command()
def pair(key: str):
    """
    Display the key-value pair.
    """
    key_val_list = check_key_value(key)
    for pair in key_val_list:
        typer.echo(f"({pair[2]}) {pair[0]}: {pair[1]}")






if __name__ == "__main__":
    app()