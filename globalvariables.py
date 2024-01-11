import configparser

def load_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return config['Variables']

# Usage example
config = load_config('config.ini')

# Accessing the variables
strategy = config['Strategy']
num_clients = int(config['Num_Clients'])
num_rounds = int(config['Num_Rounds'])
dir_parameter = float(config['Dir_parameter'])
k = float(config['K'])
r = float(config['R'])
t = float(config['T'])
p = float(config['P'])
proxy_training = config.getboolean('proxytraining')
warmup = config.getboolean('warmup')
e = int(config['E'])
currentcluster = 41
serverround = 1200
loaddatafile_txt = config['loaddatafile_txt']
centralevaluation_csv = config['centralevaluation_csv']
warmupranking_json = config['warmupranking_json']
clientclusters_csv = config['clientclusters_csv']
buildtracklist_py = config['buildtracklist_py']





























































































































































































































































































































































































































































































































