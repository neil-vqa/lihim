from typing import List
import typing
from click.termui import prompt
import typer
from .models import create_db, create_key
from .controller import *


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
    try:
        user = load_session_json()
        typer.echo(f"Current user: {user[0]}")
    except:
        typer.echo("Please login.")

@app.command()
def useradd(username: str):
    """
    'useradd [username]' -> Add a new user.
    """
    passwordx = typer.prompt("Password", hide_input=True)
    passwordy = typer.prompt("Retype password", hide_input=True)
    key_path = typer.prompt(
        f"IMPORTANT: Provide a path that will contain your key. Use absolute paths (e.g. /home/{username}/.config)"
    )
    key_name = typer.prompt(
        f"IMPORTANT: Give your key a unique name (something you'll remember but hard for others to search for)"
    )

    if passwordx == passwordy:
        try:
            key = create_key(key_path, key_name, username)
            create_user(username, passwordx, key)
            typer.echo(f"User {username} created.")
        except Exception as e:
            typer.echo(e)
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
    ),
    key_path: str = typer.Option(
        ..., prompt=True
    ),
    key_name: str = typer.Option(
        ..., prompt=True
    )
):
    """
    'login [username]' -> Login as a certain user.
    """
    try:
        enter_user(username, password, key_path, key_name)
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
    'groupadd [group name]' -> Add a new group.
    """
    try:
        response = allow_user()
        current_user = response[1]
        create_group(name, current_user)
        typer.echo(f"{name} group added.")
    except Exception as e:
        typer.echo(e)

@app.command()
def groups():
    """
    Lists all the groups of current user.
    """
    try:
        response = allow_user()
        current_user = response[1]
        groups_list = check_groups(current_user)
        for group in groups_list:
            typer.echo(group.name)
    except Exception as e:
        typer.echo(e)


@app.command()
def group(name: str):
    """
    'group [group name]' -> Lists all the keys of the group.
    """
    try:
        response = allow_user()
        current_user = response[1]
        pairs_list = check_group_pairs(name, current_user)
        for pair in pairs_list:
            typer.echo(pair.key_string)
    except Exception as e:
        typer.echo(e)

@app.command()
def pairadd():
    """
    Add a new key-value pair.
    """
    key = typer.prompt("Key")
    value = typer.prompt("Value")
    group = typer.prompt("Add to what group?")

    try:
        response = allow_user()
        current_user = response[1]
        create_pair(key, value, group, current_user)
        typer.echo(f"{key} added.")
    except Exception as e:
        typer.echo(e)

@app.command()
def pairs():
    """
    Lists all the keys of available pairs of current user.
    """
    try:
        response = allow_user()
        current_user = response[1]
        pairs_list = check_pairs(current_user)
        for pair in pairs_list:
            typer.echo(pair.key_string)
    except Exception as e:
        typer.echo(e)

@app.command()
def pair(key: str):
    """
    'pair [key]' -> Display the key-value pair.
    """
    try:
        response = allow_user()
        current_user = response[1]
        key_val_list = check_key_value(key, current_user)
        for pair in key_val_list:
            typer.echo(f"({pair[2]}) {pair[0]}: {pair[1]}")
    except Exception as e:
        typer.echo(e)

@app.command()
def groupdel(
    name: str,
    confirm: bool = typer.Option(
        ...,
        prompt="DANGER: Are you sure you want to delete this group? (Pairs within this group will also be deleted.)"
    )
):
    """
    'groupdel [group name]' -> Delete group.
    """
    if confirm:
        try:
            response = allow_user()
            current_user = response[1]
            del_response = delete_group(name, current_user)
            typer.echo("Group deleted.")
        except Exception as e:
            typer.echo(e)
    else:
        typer.echo("Cancelled.")

@app.command()
def pairdel(
    key: str, 
    group: str, 
    confirm: bool = typer.Option(
        ...,
        prompt="DANGER: Are you sure you want to delete this key-val pair?"
    )
):
    """
    'pairdel [key] [group name]' -> Delete specified key.
    """
    if confirm:
        try:
            response = allow_user()
            current_user = response[1]
            pair = load_pair_in_group(group, key, current_user)
            del_response = delete_pair(pair, current_user)
            typer.echo("Key-value pair deleted.")
        except Exception as e:
            typer.echo(e)
    else:
        typer.echo("Cancelled.")



if __name__ == "__main__":
    app()