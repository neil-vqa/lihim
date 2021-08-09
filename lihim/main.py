from typing import List
import typer
from .db import create_db, checker, create_user, check_users, enter_user


app = typer.Typer()


@app.command()
def initdb():
    create_db()
    typer.echo("Database created.")

@app.command()
def check():
    # check logged in user
    typer.echo(f"Current user:")

@app.command()
def useradd():
    username = typer.prompt("Username")
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
    try:
        enter_user(username, password)
        typer.echo(f"Logged in.")
    except Exception as e:
        typer.echo(e)
    

# @app.command()
# def groups():
#     typer.echo(print_list(group_list))


if __name__ == "__main__":
    app()