import configparser

CONFIG_PATH = 'config.ini'
CONFIG_SECTION = 'chimetime'

class CTConfig:
    def __init__(self, path=CONFIG_PATH):
        config = configparser.ConfigParser()
        config.read(path)
        self.raw_config = config[CONFIG_SECTION]

    def parse_config(self, config):
        bools = ('learning_mode', 'play_arp')
        ret = {b: config.getboolean(b) for b in bools}
        return ret
                
    def default_config(self):
        return {
                'learning_mode': True,
                'play_arp': True,
                }
