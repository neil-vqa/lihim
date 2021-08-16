"""
Contains functions used for testing.
"""

from lihim.models import User
from lihim.config import ConfigPath
import json

conf = ConfigPath()


class Helper:
    def delete_user(self, username: str):
        """
        Used mainly for cleaning database during testing.
        When the user is deleted, all the groups and pairs
        of the user are also deleted.
        """
        try:
            user = User.get(User.username==username)
            user.delete_instance(recursive=True)
        except Exception as e:
            raise e

    def clear_session(self):
        auth = {
            "LIHIM_USER": "",
            "LIHIM_PASSWORD": "",
            "LIHIM_KEY": ""
        }
        auth_dump = json.dumps(auth, indent=2)

        with open(conf.session_path, "w") as f:
            f.write(auth_dump)