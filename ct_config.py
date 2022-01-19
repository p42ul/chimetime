import asyncio
import json
import logging
import os
import time
from threading import Thread

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CTConfig:
    def __init__(self, config_path, autoreload=True):
        config_path = os.path.abspath(config_path)
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Can't open {config_path} for reading.")
        self.config_path = config_path
        self.config = None # reminder that this member exists
        self.load_config() # sets self.config
        if autoreload:
            t = Thread(target=self.autoreload, daemon=True)
            t.start()

    # Autoreload function to be called in a thread.
    def autoreload(self):
        observer = Observer()
        event_handler = AutoReloadEventHandler(self.load_config, filename=self.config_path, args=[])
        observer.schedule(event_handler, os.path.dirname(self.config_path), recursive=False)
        observer.start()
        logging.info('Config autoreload daemon thread started.')
        while True:
            time.sleep(1)

    def load_config(self):
        logging.info(f'reading config file at {self.config_path}')
        with open(self.config_path, 'r') as f:
            text = f.read()
            self.config = json.loads(text)

    def save_config(self, config: dict):
        with open(self.config_path, 'w') as f:
            f.write(json.dumps(config))

    def default_config(self):
        # If you change a value here, be sure to add it to the
        # included config.ini file, and vice versa.
        return {'play_arp': True,
                'arp_delay': 1.0,
                'polling_interval': 0.01,
                'interdigit_delay': 0.5,
                'arp_interdigit_delay': 0.15,
                }

    def as_dict(self):
        return self.config

    def __getitem__(self, key):
        return self.config[key]


class AutoReloadEventHandler(FileSystemEventHandler):
    def __init__(self, callback, args, filename):
        self.callback = callback
        self.args = args
        self.filename = filename

    def on_modified(self, event):
        if event.src_path == self.filename:
            self.callback(*self.args)
