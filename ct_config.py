import configparser

# Default config file path.
CONFIG_PATH = 'config.ini'
# The section header name to read.
CONFIG_SECTION = 'chimetime'

class CTConfig:
    def __init__(self, path=CONFIG_PATH):
        load_config(path)

    def load_config(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        config = config[CONFIG_SECTION]
        self.config = self.parse_config(config)

    def parse_config(self, config):
        return {
            'play_arp': config.getboolean('play_arp'),
            'learning_mode': config.getboolean('learning_mode')
            }

    def __getitem__(self, key):
        return self.config[key]
