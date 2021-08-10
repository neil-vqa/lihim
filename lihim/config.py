import os
from pathlib import Path


class ConfigPath:
    home = str(Path.home())
    config_path = f"{home}/.config/lihim"
    db_path = f"{config_path}/lihimdb.db"
    session_path = f"{config_path}/session.json"

    def create_config(self):
        os.makedirs(self.config_path, exist_ok = True)
