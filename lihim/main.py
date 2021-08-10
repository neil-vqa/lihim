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
    Add a new user.
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
    Login as a certain user.
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
    Add a new group.
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
    Lists groups of current user.
    """
    groups_list = check_groups()
    for group in groups_list:
        typer.echo(group.name)

@app.command()
def pairadd():
    key = typer.prompt("Key")
    value = typer.prompt("Value")
    group = typer.prompt("Add to what group?")

    try:
        allow_user()
        create_pair(key, value, group)
        typer.echo(f"{key} added.")
    except Exception as e:
        typer.echo(e)

if __name__ == "__main__":
    app()