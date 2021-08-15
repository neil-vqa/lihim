from peewee import Value
from lihim.main import app
from typer.testing import CliRunner
import string
import random


runner = CliRunner()

def test_initialize_db():
    result = runner.invoke(app, ["initdb"])
    assert result.exit_code == 0
    assert "Database created." in result.stdout

def test_check_pass():
    result = runner.invoke(app, ["check"])
    assert result.exit_code == 0
    assert "Current user:" in result.stdout

def test_useradd_pass():
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))

    result = runner.invoke(
        app,
        ["useradd", f"{username}"], 
        input=f"password\npassword\n/home/neeban/shipt\n{username}_key"
    )
    assert result.exit_code == 0
    assert f"User {username} created." in result.stdout

def test_useradd_fail_already_exists():
    result = runner.invoke(
        app,
        ["useradd", "hyojoo"], 
        input="password\npassword\n/home/neeban/shipt\nhyojoo_key"
    )
    assert result.exit_code == 0
    assert "User hyojoo already exists." in result.stdout

def test_useradd_fail_password_mismatch():
    result = runner.invoke(
        app,
        ["useradd", "hyojoo"], 
        input="passworx\npasswory\n/home/neeban/shipt\nhyojoo_key"
    )
    assert result.exit_code == 0
    assert "Password did not match. Please try again." in result.stdout

def test_users():
    result = runner.invoke(app, ["users"])
    assert result.exit_code == 0

def test_login_pass():
    result = runner.invoke(
        app, 
        ["login", "jihyo"],
        input="love\n/home/neeban/shipt\njihyo_key"
    )
    assert result.exit_code == 0
    assert "Logged in." in result.stdout

def test_logout_pass():
    result = runner.invoke(app, ["logout"])
    assert result.exit_code == 0
    assert "Logged out. Bye!" in result.stdout

def test_groupadd_pass():
    runner.invoke(
        app, 
        ["login", "jihyo"],
        input="love\n/home/neeban/shipt\njihyo_key"
    )

    group_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))

    result = runner.invoke(app, ["groupadd", f"{group_name}"])
    assert result.exit_code == 0
    assert f"{group_name} group added." in result.stdout

def test_groups():
    result = runner.invoke(app, ["groups"])
    assert result.exit_code == 0

def test_group_show_list_of_pairs():
    result = runner.invoke(app, ["group", "twice"])
    assert result.exit_code == 0

def test_pairadd_pass():
    key = ''.join(random.choices(string.ascii_uppercase, k=7))
    Value = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
    group = "twice"

    result = runner.invoke(
        app, 
        ["pairadd"],
        input=f"{key}\n{Value}\n{group}"
    )
    assert result.exit_code == 0
    assert f"{key} added." in result.stdout

def test_pairs():
    result = runner.invoke(app, ["pairs"])
    assert result.exit_code == 0

def test_pair_show_key_value():
    result = runner.invoke(app, ["pair","fancy"])
    assert result.exit_code == 0
    assert "(twice) fancy: wooooooohhhhh" in result.stdout

def test_groupdel_yes_pass():
    group_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
    runner.invoke(app, ["groupadd", f"{group_name}"])

    result = runner.invoke(
        app, 
        ["groupdel",f"{group_name}"],
        input="y"
    )
    assert result.exit_code == 0
    assert "Group deleted." in result.stdout

def test_groupdel_no_pass():
    result = runner.invoke(
        app, 
        ["groupdel","test_group"],
        input="n"
    )
    assert result.exit_code == 0
    assert "Cancelled" in result.stdout