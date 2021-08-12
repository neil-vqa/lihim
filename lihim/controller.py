import json
import nacl.pwhash
import nacl.secret
import nacl.utils
from typing import Optional
from .config import ConfigPath
from .models import User, Group, Pair


conf = ConfigPath()

"""
CLI commands associated with users use these functions.
"""

def use_key(key: str, encrypt_text: Optional[str] = None, decrypt_text: Optional[bytes] = None):
    with open(key, "rb") as f:
        key_bin = f.read()
        box = nacl.secret.SecretBox(key_bin)
    
    if encrypt_text:
        encoded_text = encrypt_text.encode('UTF-8')
        encrypted_text = box.encrypt(encoded_text)
        return encrypted_text
    elif decrypt_text:
        plaintext = box.decrypt(decrypt_text)
        decoded_text = plaintext.decode('UTF-8')
        return decoded_text

def create_user(username: str, password: str, key: str) -> None:
    password_byte = password.encode('UTF-8')
    hashed_password = nacl.pwhash.str(password_byte)

    new_user = User(
        username=username, 
        password=hashed_password
    )
    new_user.save()

def check_users():
    users = User.select()
    return users

"""
Functions associated with managing the session.
"""
    
def enter_user(username: str, password: str, key_path: str):
    """
    Writes the entered username and password to session.json when logging in.
    """
    key = f"{key_path}/lihimkey_{username}"

    auth = {
        "LIHIM_USER": username,
        "LIHIM_PASSWORD": password,
        "LIHIM_KEY": key
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
    """
    Gets the User instance for current_user variable.
    """
    try:
        user = User.get(User.username==username)
        return user
    except:
        raise ValueError("User does not exist. Unauthenticated.")

def check_password(current_user, password):
    """
    Verifies the password in session.json against
    the hashed password in the database.
    """
    correct = current_user.password.encode('UTF-8')
    entered = password.encode('UTF-8')

    try:
        nacl.pwhash.verify(correct, entered)
    except Exception as e:
        raise e

def allow_user():
    """
    Check if authenticated.
    """
    username, password = load_session_json()

    try:
        current_user = get_user(username)
        check_password(current_user, password)
        return (True, current_user)
    except Exception as e:
        raise e

def clear_user():
    """
    Clears username and password in session.json.
    """
    auth = {
        "LIHIM_USER": "",
        "LIHIM_PASSWORD": "",
        "LIHIM_KEY": ""
    }
    auth_dump = json.dumps(auth, indent=2)

    with open(conf.session_path, "w") as f:
        f.write(auth_dump)


""" 
CLI commands associated with groups and pairs
use these functions.
"""

def create_group(name: str, current_user: User):
    new_group = Group(
        name=name,
        user=current_user
    )
    new_group.save()

def check_groups(current_user: User):
    groups = current_user.groups
    return groups

def check_group_pairs(name: str, current_user: User):
    try:
        group = Group.get(Group.user==current_user, Group.name==name)
        return group.pairs
    except Group.DoesNotExist:
        raise ValueError("Group does not exist.")

def create_pair(key: str, value: str, group: str, current_user: User):
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

def check_pairs(current_user: User):
    pairs = current_user.pairs
    return pairs

def check_key_value(key: str, current_user: User):
    pairs = current_user.pairs
    key_val = [(pair.key_string, pair.value_string, pair.group.name) for pair in pairs if pair.key_string == key]
    return key_val
    
def load_pair_in_group(group_name: str, key: str, current_user: User):
    try:
        pair_in_group = Group.get(Group.user==current_user, Group.name==group_name)
        pair = Pair.get(Pair.user==current_user, Pair.group==pair_in_group, Pair.key_string==key)
        return pair
    except Group.DoesNotExist:
        raise ValueError("Group does not exist.")
    except Pair.DoesNotExist:
        raise ValueError("Pair does not exist.")

def delete_group(name: str, current_user: User):
    try:
        group = Group.get(Group.user==current_user, Group.name==name)
        group.delete_instance(recursive=True)
    except Group.DoesNotExist:
        raise ValueError("Group does not exist.")
    except Exception as e:
        raise e

def delete_pair(pair: Pair, current_user: User):
    try:
        pair.delete_instance()
    except Exception as e:
        raise e