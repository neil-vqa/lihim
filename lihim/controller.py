import json
import nacl.pwhash
import nacl.secret
import nacl.utils
import errno
import os
from typing import overload, Tuple, List
from peewee import ModelSelect
from .config import ConfigPath
from .models import User, Group, Pair
from pathlib import Path


conf = ConfigPath()

"""
CLI commands associated with users use these functions.
"""

@overload
def use_key(key: str, encrypt_text: str) -> nacl.utils.EncryptedMessage: ...

@overload
def use_key(key: str, decrypt_text: bytes) -> str: ...

def use_key(key, encrypt_text = None, decrypt_text = None):
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

def load_key() -> str:
    try:
        with open(conf.session_path, "r") as f:
            current_user = json.load(f)

        key_file = current_user['LIHIM_KEY']
        return key_file
    except Exception as e:
        raise e
    
def check_key_exists(key: str) -> None:
    try:
        key_file = Path(key)
        if not key_file.exists():
            clear_user()
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), "Key not found.")
    except Exception as e:
        raise e

def create_user(username: str, password: str, key: str) -> None:
    password_byte = password.encode('UTF-8')
    hashed_password = nacl.pwhash.str(password_byte)

    try:
        new_user = User(
            username=username, 
            password=hashed_password
        )
        new_user.save()
    except Exception as e:
        raise e

def check_users() -> ModelSelect:
    users = User.select()
    return users

"""
Functions associated with managing the session.
"""
    
def enter_user(username: str, password: str, key_path: str, key_name: str) -> None:
    """
    Writes the entered username and password to session.json when logging in.
    """
    key = f"{key_path}/{key_name}"

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
        check_key_exists(key)
    except Exception as e:
        raise e

def load_session_json() -> Tuple[str, str]:
    try:
        with open(conf.session_path, "r") as f:
            current_user = json.load(f)

        username = current_user['LIHIM_USER']
        password = current_user['LIHIM_PASSWORD']

        return username, password
    except Exception as e:
        raise e

def get_user(username) -> User:
    """
    Gets the User instance for current_user variable.
    """
    try:
        user = User.get(User.username==username)
        return user
    except:
        raise ValueError("User does not exist. Unauthenticated.")

def check_password(current_user, password) -> None:
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

def allow_user() -> Tuple[bool, User]:
    """
    Check if authenticated.
    """
    try:
        username, password = load_session_json()
        current_user = get_user(username)
        check_password(current_user, password)
        return (True, current_user)
    except Exception as e:
        raise e

def clear_user() -> None:
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

def create_group(name: str, current_user: User) -> None:
    try:
        new_group = Group(
            name=name,
            user=current_user
        )
        new_group.save()
    except Exception as e:
        raise e

def check_groups(current_user: User) -> ModelSelect:
    groups = current_user.groups
    return groups

def check_group_pairs(name: str, current_user: User) -> ModelSelect:
    try:
        group = Group.get(Group.user==current_user, Group.name==name)
        return group.pairs
    except Group.DoesNotExist:
        raise ValueError("Group does not exist.")

def create_pair(key: str, value: str, group: str, current_user: User) -> None:
    try:
        group_to_add = Group.get(Group.user==current_user, Group.name==group)
        key_file = load_key()
        encrypted_value = use_key(key_file, encrypt_text=value)
        new_pair = Pair(
            key_string=key,
            value_string=encrypted_value,
            group=group_to_add,
            user=current_user
        )
        new_pair.save()
    except Group.DoesNotExist:
        raise ValueError("Group does not exist.")
    except Exception as e:
        raise e

def check_pairs(current_user: User) -> ModelSelect:
    pairs = current_user.pairs
    return pairs

def check_key_value(key: str, current_user: User) -> List[Tuple[str, str, str]]:
    key_file = load_key()
    pairs = current_user.pairs
    key_val = [(pair.key_string, use_key(key_file, decrypt_text=pair.value_string), pair.group.name) for pair in pairs if pair.key_string == key]
    return key_val
    
def load_pair_in_group(group_name: str, key: str, current_user: User) -> Pair:
    try:
        pair_in_group = Group.get(Group.user==current_user, Group.name==group_name)
        pair = Pair.get(Pair.user==current_user, Pair.group==pair_in_group, Pair.key_string==key)
        return pair
    except Group.DoesNotExist:
        raise ValueError("Group does not exist.")
    except Pair.DoesNotExist:
        raise ValueError("Pair does not exist.")

def delete_group(name: str, current_user: User) -> None:
    try:
        group = Group.get(Group.user==current_user, Group.name==name)
        group.delete_instance(recursive=True)
    except Group.DoesNotExist:
        raise ValueError("Group does not exist.")
    except Exception as e:
        raise e

def delete_pair(pair: Pair, current_user: User) -> None:
    try:
        pair.delete_instance()
    except Exception as e:
        raise e