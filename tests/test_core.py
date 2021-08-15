from lihim.main import app
from typer.testing import CliRunner


runner = CliRunner()

def test_initialize_db():
    result = runner.invoke(app, ["initdb"])
    assert result.exit_code == 0
    assert "Database created." in result.stdout

def test_check_pass():
    result = runner.invoke(app, ["check"])
    assert result.exit_code == 0
    assert "Current user:" in result.stdout

# def test_useradd_pass():
#     result = runner.invoke(
#         app,
#         ["useradd", "hyojoo"], 
#         input="password\npassword\n/home/neeban/shipt\nhyojoo_key"
#     )
#     assert result.exit_code == 0
#     assert "User hyojoo created." in result.stdout

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