from typing import List
import typer
from .db import create_db, create_user, check_users, enter_user, clear_user, allow_user, load_session_json


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
def groupadd():
    """
    Add a new group.
    """
    try:
        allow_user()
        typer.echo("new group added.")
    except Exception as e:
        typer.echo(e)


if __name__ == "__main__":
    app()