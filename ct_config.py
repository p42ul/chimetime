import configparser
import os

# Default config file path.
CONFIG_PATH = 'config.ini'
# The section header name to read.
CONFIG_SECTION = 'chimetime'

class CTConfig:
    def __init__(self, path=None):
        if path is None:
            path = CONFIG_PATH
        if not os.path.exists(path):
            raise FileNotFoundError(f"Can't open {path} for reading.")
        self.load_config(path)

    def load_config(self, path):
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
