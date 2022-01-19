import asyncio
import configparser
import logging
import os
import time
from threading import Thread

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# The section header name to read.
CONFIG_SECTION = 'chimetime'

class CTConfig:
    def __init__(self, config_path, autoreload=True):
        config_path = os.path.abspath(config_path)
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Can't open {config_path} for reading.")
        self.load_config(config_path)
        if autoreload:
            t = Thread(target=self.autoreload, args=[config_path], daemon=True)
            t.start()

    # Autoreload function to be called in a thread.
    def autoreload(self, config_path):
        observer = Observer()
        event_handler = AutoReloadEventHandler(
            self.load_config, args=[config_path], filename=config_path)
        observer.schedule(event_handler, os.path.dirname(config_path), recursive=False)
        observer.start()
        while True:
            time.sleep(1)

    def load_config(self, config_path):
        logging.info(f'reading config file at {config_path}')
        config = configparser.ConfigParser()
        config.read(config_path)
        config_section = config[CONFIG_SECTION]
        self.config = self.parse_config_section(config_section)

    def default_config(self):
        # If you change a value here, be sure to add it to the
        # included config.ini file, and vice versa.
        return {'play_arp': True,
                'arp_delay': 1.0,
                'polling_interval': 0.01,
                'interdigit_delay': 0.5,
                'arp_interdigit_delay': 0.15,
                }

    def parse_config_section(self, config_section):
        ret = self.default_config()
        for k, v in self.default_config().items():
            t = type(v)
            maybe = None
            if t is bool:
                maybe = config_section.getboolean(k)
            elif t is float:
                maybe = config_section.getfloat(k)
            elif t is int:
                maybe = config_section.getint(k)
            else:
                maybe = config_section.get(k)
            if maybe is not None:
                ret[k] = maybe
        return ret

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
