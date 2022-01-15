import configparser

CONFIG_PATH = 'config.ini'

class CTConfig:
    def __init__(self, path=CONFIG_PATH):
        config = configparser.ConfigParser()
        config.read(path)
        self.config=config

    def parse_config(self, config):
        

    def default_config(self):
        return {
                'learning_mode': True,
                'play_arp': True,
                }
