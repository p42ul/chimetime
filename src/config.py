from constants import CONFIG_PATH

import json
import logging
import os

class Config:
    def __init__(self):
        config_path = os.path.abspath(CONFIG_PATH)
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Can't open {config_path} for reading.")
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        logging.info(f'reading config file at {self.config_path}')
        with open(self.config_path, 'r') as f:
            text = f.read()
            return json.loads(text)

    def save_config(self, config: dict):
        with open(self.config_path, 'w') as f:
            f.write(json.dumps(config, indent=2)) # indent to make it easier to read

    def as_dict(self):
        return self.config

    def __getitem__(self, key):
        return self.config[key]