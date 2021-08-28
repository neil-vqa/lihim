from lihim.main import app
from typer.testing import CliRunner
from .helper import Helper
from pathlib import Path
import string
import random


runner = CliRunner()
helper = Helper()
home = str(Path.home())


def test_initialize_db():
    result = runner.invoke(app, ["initdb"])
    assert result.exit_code == 0
    assert "Database created." in result.stdout


def test_check_pass():
    runner.invoke(
        app,
        ["useradd", "hyojoo"],
        input=f"password\npassword\n/{home}\nhyojoo_key_test",
    )

    result = runner.invoke(
        app, ["login", "hyojoo"], input=f"password\n/{home}\nhyojoo_key_test"
    )

    result = runner.invoke(app, ["check"])
    helper.delete_user("hyojoo")
    helper.clear_session()

    assert result.exit_code == 0
    assert "Current user: hyojoo" in result.stdout


def test_useradd_pass():
    result = runner.invoke(
        app,
        ["useradd", "hyojoo"],
        input=f"password\npassword\n/{home}\nhyojoo_key_test",
    )
    helper.delete_user("hyojoo")

    assert result.exit_code == 0
    assert f"User hyojoo created." in result.stdout


def test_useradd_fail_already_exists():
    runner.invoke(
        app,
        ["useradd", "hyojoo"],
        input=f"password\npassword\n/{home}\nhyojoo_key_test",
    )

    result = runner.invoke(
        app,
        ["useradd", "hyojoo"],
        input=f"password\npassword\n/{home}\nhyojoo_key_test",
    )
    helper.delete_user("hyojoo")

    assert result.exit_code == 0
    assert "User hyojoo already exists." in result.stdout


def test_useradd_fail_password_mismatch():
    runner.invoke(
        app,
        ["useradd", "hyojoo"],
        input=f"password\npassword\n/{home}\nhyojoo_key_test",
    )

    result = runner.invoke(
        app,
        ["useradd", "hyojoo"],
        input=f"passworx\npasswory\n/{home}\nhyojoo_key_test",
    )
    helper.delete_user("hyojoo")

    assert result.exit_code == 0
    assert "Password did not match. Please try again." in result.stdout


def test_users():
    runner.invoke(
        app,
        ["useradd", "hyojoo"],
        input=f"password\npassword\n/{home}\nhyojoo_key_test",
    )

    result = runner.invoke(app, ["users"])
    helper.delete_user("hyojoo")

    assert result.exit_code == 0
    assert "hyojoo" in result.stdout


def test_login_pass():
    runner.invoke(
        app,
        ["useradd", "hyojoo"],
        input=f"password\npassword\n/{home}\nhyojoo_key_test",
    )

    result = runner.invoke(
        app, ["login", "hyojoo"], input=f"password\n/{home}\nhyojoo_key_test"
    )
    helper.delete_user("hyojoo")
    helper.clear_session()

    assert result.exit_code == 0
    assert "Logged in." in result.stdout


def test_logout_pass():
    result = runner.invoke(app, ["logout"])
    assert result.exit_code == 0
    assert "Logged out. Bye!" in result.stdout


def test_groupadd_pass():
    runner.invoke(
        app,
        ["useradd", "hyojoo"],
        input=f"password\npassword\n/{home}\nhyojoo_key_test",
    )

    runner.invoke(app, ["login", "hyojoo"], input=f"password\n/{home}\nhyojoo_key_test")

    group_name = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))

    result = runner.invoke(app, ["groupadd", f"{group_name}"])
    helper.delete_user("hyojoo")
    helper.clear_session()

    assert result.exit_code == 0
    assert f"{group_name} group added." in result.stdout


def test_groups():
    runner.invoke(
        app,
        ["useradd", "hyojoo"],
        input=f"password\npassword\n/{home}\nhyojoo_key_test",
    )

    runner.invoke(app, ["login", "hyojoo"], input=f"password\n/{home}\nhyojoo_key_test")

    group_name = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))

    runner.invoke(app, ["groupadd", f"{group_name}"])

    result = runner.invoke(app, ["groups"])
    helper.delete_user("hyojoo")
    helper.clear_session()

    assert result.exit_code == 0
    assert f"{group_name}" in result.stdout


def test_group_show_list_of_pairs():
    runner.invoke(
        app,
        ["useradd", "hyojoo"],
        input=f"password\npassword\n/{home}\nhyojoo_key_test",
    )

    runner.invoke(app, ["login", "hyojoo"], input=f"password\n/{home}\nhyojoo_key_test")

    key = "".join(random.choices(string.ascii_uppercase, k=7))
    Value = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))
    group_name = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))

    runner.invoke(app, ["groupadd", f"{group_name}"])

    runner.invoke(app, ["pairadd"], input=f"{key}\n{Value}\n{group_name}")

    result = runner.invoke(app, ["group", f"{group_name}"])
    helper.delete_user("hyojoo")
    helper.clear_session()

    assert result.exit_code == 0
    assert f"{key}" in result.stdout


def test_pairadd_pass():
    runner.invoke(
        app,
        ["useradd", "hyojoo"],
        input=f"password\npassword\n/{home}\nhyojoo_key_test",
    )

    runner.invoke(app, ["login", "hyojoo"], input=f"password\n/{home}\nhyojoo_key_test")

    key = "".join(random.choices(string.ascii_uppercase, k=7))
    Value = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))
    group_name = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))

    runner.invoke(app, ["groupadd", f"{group_name}"])

    result = runner.invoke(app, ["pairadd"], input=f"{key}\n{Value}\n{group_name}")
    helper.delete_user("hyojoo")
    helper.clear_session()

    assert result.exit_code == 0
    assert f"{key} added." in result.stdout


def test_pairs():
    runner.invoke(
        app,
        ["useradd", "hyojoo"],
        input=f"password\npassword\n/{home}\nhyojoo_key_test",
    )

    runner.invoke(app, ["login", "hyojoo"], input=f"password\n/{home}\nhyojoo_key_test")

    key = "".join(random.choices(string.ascii_uppercase, k=7))
    Value = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))
    group_name = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))

    runner.invoke(app, ["groupadd", f"{group_name}"])

    runner.invoke(app, ["pairadd"], input=f"{key}\n{Value}\n{group_name}")

    result = runner.invoke(app, ["pairs"])
    helper.delete_user("hyojoo")
    helper.clear_session()

    assert result.exit_code == 0
    assert f"{key}" in result.stdout


def test_pair_show_key_value():
    runner.invoke(
        app,
        ["useradd", "hyojoo"],
        input=f"password\npassword\n/{home}\nhyojoo_key_test",
    )

    runner.invoke(app, ["login", "hyojoo"], input=f"password\n/{home}\nhyojoo_key_test")

    key = "".join(random.choices(string.ascii_uppercase, k=7))
    Value = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))
    group_name = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))

    runner.invoke(app, ["groupadd", f"{group_name}"])

    runner.invoke(app, ["pairadd"], input=f"{key}\n{Value}\n{group_name}")

    result = runner.invoke(app, ["pair", f"{key}"])
    helper.delete_user("hyojoo")
    helper.clear_session()

    assert result.exit_code == 0
    assert f"({group_name}) {key}: {Value}" in result.stdout


def test_groupdel_yes_pass():
    runner.invoke(
        app,
        ["useradd", "hyojoo"],
        input=f"password\npassword\n/{home}\nhyojoo_key_test",
    )

    runner.invoke(app, ["login", "hyojoo"], input=f"password\n/{home}\nhyojoo_key_test")

    group_name = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))
    runner.invoke(app, ["groupadd", f"{group_name}"])

    result = runner.invoke(app, ["groupdel", f"{group_name}"], input="y")
    helper.delete_user("hyojoo")
    helper.clear_session()

    assert result.exit_code == 0
    assert "Group deleted." in result.stdout


def test_groupdel_no_pass():
    result = runner.invoke(app, ["groupdel", "test_group"], input="n")
    assert result.exit_code == 0
    assert "Cancelled" in result.stdout


def test_pairdel_yes_pass():
    runner.invoke(
        app,
        ["useradd", "hyojoo"],
        input=f"password\npassword\n/{home}\nhyojoo_key_test",
    )

    runner.invoke(app, ["login", "hyojoo"], input=f"password\n/{home}\nhyojoo_key_test")

    key = "".join(random.choices(string.ascii_uppercase, k=7))
    Value = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))
    group_name = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))

    runner.invoke(app, ["groupadd", f"{group_name}"])

    runner.invoke(app, ["pairadd"], input=f"{key}\n{Value}\n{group_name}")

    result = runner.invoke(app, ["pairdel", f"{key}", f"{group_name}"], input="y")
    helper.delete_user("hyojoo")
    helper.clear_session()

    assert result.exit_code == 0
    assert "Key-value pair deleted." in result.stdout


def test_pairdel_no_pass():
    result = runner.invoke(app, ["pairdel", "test_key", "test_group"], input="n")

    assert result.exit_code == 0
    assert "Cancelled" in result.stdout
