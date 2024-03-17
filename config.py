"""Contains the static Config class.
To reset the config file, run this module."""
import configparser

class Config:
    """Read and get configuration"""
    config:configparser.ConfigParser = configparser.ConfigParser()
    @staticmethod
    def load_config():
        """Load configuration settings."""
        try:
            Config.config.read('config.ini')
        except (KeyError, configparser.MissingSectionHeaderError):
            Config.write_default()
    @staticmethod
    def write_default():
        """Create default configuration settings"""
        Config.config['Screen'] = {'fps' : '5', 'scale' : '5', 'filter' : '2'}
        Config.config['Poop'] = {'interval' : 10, 'max' : 5}
        Config.config['Debug'] = {'text' : False, 'images':False}
        Config.config['Database'] = {'database': '',
                                     'user': '',
                                     'password': '',
                                     'host': '',
                                     'port': ''}
        with open('config.ini', 'w', encoding="utf8") as configfile:
            Config.config.write(configfile)

if __name__ == '__main__':
    Config.write_default()
    print ("default config written")
