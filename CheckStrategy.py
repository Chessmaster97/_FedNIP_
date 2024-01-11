import configparser

def check_strategy():
    config = configparser.ConfigParser()
    config.read('config.ini')

    strategy = config.get('Variables', 'Strategy')
    return strategy

