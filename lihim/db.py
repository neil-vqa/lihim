import json
import nacl.pwhash
import nacl.secret
import nacl.utils
from .config import ConfigPath
from .models import User, Group, Pair


conf = ConfigPath()

def create_user(username: str, password: str) -> None:
    password_byte = password.encode('UTF-8')
    hashed_password = nacl.pwhash.str(password_byte)

    key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)

    new_user = User(
        username=username, 
        password=hashed_password,
        box_key=key
    )
    new_user.save()

def check_users():
    users = User.select()
    return users
    
def enter_user(username: str, password: str):
    auth = {
        "LIHIM_USER": username,
        "LIHIM_PASSWORD": password
    }
    auth_dump = json.dumps(auth, indent=2)

    with open(conf.session_path, "w") as f:
        f.write(auth_dump)

    try:
        allow_user()
    except Exception as e:
        raise e

def load_session_json():
    with open(conf.session_path, "r") as f:
        current_user = json.load(f)

    username = current_user['LIHIM_USER']
    password = current_user['LIHIM_PASSWORD']

    return username, password

def get_user(username):
    try:
        user = User.get(User.username==username)
        return user
    except:
        raise ValueError("User does not exist.")

def check_password(current_user, password):
    correct = current_user.password.encode('UTF-8')
    entered = password.encode('UTF-8')

    try:
        nacl.pwhash.verify(correct, entered)
    except Exception as e:
        raise e

def allow_user():
    username, password = load_session_json()

    try:
        current_user = get_user(username)
        check_password(current_user, password)
        return True
    except Exception as e:
        raise e

def clear_user():
    auth = {
        "LIHIM_USER": "",
        "LIHIM_PASSWORD": ""
    }
    auth_dump = json.dumps(auth, indent=2)

    with open(conf.session_path, "w") as f:
        f.write(auth_dump)

def create_group(name: str):
    credentials = load_session_json()
    current_user = get_user(credentials[0])

    new_group = Group(
        name=name,
        user=current_user
    )
    new_group.save()

def check_groups():
    credentials = load_session_json()
    current_user = get_user(credentials[0])
    groups = current_user.groups
    return groups

def create_pair(key: str, value: str, group: str):
    credentials = load_session_json()
    current_user = get_user(credentials[0])

    try:
        group_to_add = Group.get(Group.user==current_user, Group.name==group)
        new_pair = Pair(
            key_string=key,
            value_string=value,
            group=group_to_add,
            user=current_user
        )
        new_pair.save()
    except Exception as e:
        raise e
