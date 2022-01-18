import asyncio
import configparser
import logging
import os
import time
from threading import Thread

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Default config file path.
CONFIG_PATH = 'config.ini'
# The section header name to read.
CONFIG_SECTION = 'chimetime'

class CTConfig:
    def __init__(self, path=None, autoreload=True):
        if path is None:
            curdir = os.path.abspath(os.path.dirname(__file__))
            path = os.path.join(curdir, CONFIG_PATH)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Can't open {path} for reading.")
        self.load_config(path)
        if autoreload:
            t = Thread(target=self.autoreload, args=[path], daemon=True)
            t.start()

    def print_it(self, p):
        print(p)

    # Autoreload function to be called in a thread.
    def autoreload(self, path):
        observer = Observer()
        event_handler = AutoReloadEventHandler(
            self.load_config, args=[path], filename=path)
        observer.schedule(event_handler, os.path.dirname(path), recursive=False)
        observer.start()
        while True:
            time.sleep(1)

    def load_config(self, path):
        logging.info(f'reading config file at {path}')
        config = configparser.ConfigParser()
        config.read(path)
        config = config[CONFIG_SECTION]
        self.config = self.parse_config(config)

    def default_config(self):
        # If you change a value here, be sure to add it to the
        # included config.ini file, and vice versa.
        return {'play_arp': True,
                'arp_delay': 1.0,
                'polling_interval': 0.01,
                'interdigit_delay': 0.5,
                'arp_interdigit_delay': 0.15,
                }

    def parse_config(self, config):
        ret = self.default_config()
        for k, v in self.default_config().items():
            t = type(v)
            maybe = None
            if t is bool:
                maybe = config.getboolean(k)
            elif t is float:
                maybe = config.getfloat(k)
            elif t is int:
                maybe = config.getint(k)
            else:
                maybe = config.get(k)
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
