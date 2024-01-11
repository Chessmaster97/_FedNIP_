from flwr.common import Metrics

import CheckStrategy
import RemoveGlobalweights
import calculate_average_weights
import emptyLogSwaps
import filenameforserver
import findclusterid
import getheighestrankedclient
import getserverround
import globalvariables
import removefilesnames
import resultsFEDNIP
import setserverround
import updaterankings
import updatetracklist
from checkspecialtraining import check_special_training
import DataGlobalModel
import DataLoad
import Loaddata;
import FedNIP;
from collections import OrderedDict
from typing import Dict, List, Optional, Tuple
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import flwr as fl
import torch
from Client import client_fn
from NeuralNet import set_parameters,get_parameters,train,test, Net
from globalvariables import num_rounds,num_clients,e,proxy_training
import copy
import time
DEVICE = torch.device("cpu")

import os

# Define the file path
weights_file_path = "weightsglobal.pth"

# Check if the file exists
if os.path.exists(weights_file_path):
    # If it exists, remove it
    os.remove(weights_file_path)

globalnet = Net().to(DEVICE)
torch.save(get_parameters(globalnet), f"weightsglobal.pth")


# Specify client resources, GPU (defaults to 1 CPU and 0 GPU)
client_resources = None
if DEVICE.type == "cuda":
    client_resources = {"num_gpus": 1}

def fit_config(server_round: int):
    """Return training configuration dict for each round.

    Perform two rounds of training with one local epoch, increase to two local
    epochs afterwards.
    """
    config = {
        "server_round": server_round,  # The current round of federated learning
        "local_epochs": e, #if server_round < 2 else 2,  #
    }

    def set_server_round(new_value):
        with open('globalvariables.py', 'r') as file:
            lines = file.readlines()

        with open('globalvariables.py', 'w') as file:
            for line in lines:
                if line.startswith('serverround'):
                    file.write(f'serverround = {new_value}\n')
                else:
                    file.write(line)
    set_server_round(server_round)

    return config

def empty_json_file(filename):
    with open(filename, 'w') as file:
        file.write("")

def empty_text_file(filename):
    with open(filename, 'w') as file:
        file.write('')

def get_evaluate_fn():

    server_round = getserverround.get_server_round('globalvariables.py')
    testloader = torch.load(f'testloader.pth')
    import delresults
    delresults.empty_csv_file("resultsFedAvg.csv")
    removefilesnames.remove_client_files("client", num_clients)
    #RemoveGlobalweights.remove_file("weightsglobal.pth")
    setserverround.set_server_round()
    print(server_round)
    print(globalvariables.warmup)
    print(globalvariables.strategy)

    def evaluate(server_round1,parameters,config):
        server_round = getserverround.get_server_round('globalvariables.py')
        if server_round == 0:
            print("I came to here")
            return 0, {"accuracy": 0}
        else:

            avg_weights = calculate_average_weights.calculate_average_weights()
            set_parameters(globalnet, avg_weights)  # Update model with the best parameters
            loss, accuracy = test(globalnet, testloader)
            print(f"Server-side evaluation loss {loss} / accuracy {accuracy}")
            removefilesnames.remove_client_files("client",num_clients)
            os.remove("weightsglobal.pth")
            torch.save(get_parameters(globalnet), f"weightsglobal.pth")
            # Read the content of the file into a variable
            with open('filenameserver.txt', 'r') as file:

                filename = file.read()
            resultsFEDNIP.write_to_csv(filename, server_round, round(accuracy, 4))
            return loss, {"accuracy": accuracy}


    return evaluate

params = get_parameters(Net())

strategy = FedNIP.FedNIP(
    min_fit_clients=num_clients,
    min_evaluate_clients=num_clients,
    min_available_clients=num_clients,
    evaluate_fn=get_evaluate_fn(),
    on_fit_config_fn=fit_config,
    initial_parameters=fl.common.ndarrays_to_parameters(params),
)

fl.simulation.start_simulation(
    client_fn=client_fn,
    num_clients=num_clients,
    config=fl.server.ServerConfig(num_rounds= num_rounds),
    strategy=strategy,
    client_resources=client_resources,
)