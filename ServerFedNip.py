from flwr.common import Metrics

import RemoveGlobalweights
import emptyLogSwaps
import filenameforserver
import findbestfilepath
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
from EMD_calculator import calculateEMD
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

import json

import json

def update_client_accuracy(file_path, client_id, new_accuracy):
    # Read the existing data from the JSON file
    with open(file_path, "r") as file:
        existing_data = json.load(file)

    # Update the accuracy for the specific client
    for client in existing_data:
        if client["clientID"] == int(client_id):
            client["accuracy"] = new_accuracy
            break

    #Write the updated data back to the JSON file
    with open(file_path, "w") as file:
        json.dump(existing_data, file, indent=4)

def empty_json_file(filename):
    with open(filename, 'w') as file:
        file.write("")

def empty_text_file(filename):
    with open(filename, 'w') as file:
        file.write('')

def get_evaluate_fn():

    server_round = getserverround.get_server_round('globalvariables.py')
    testloader = torch.load(f'testloader.pth')
    for i in range(0, num_clients):
        # Usage example
        empty_json_file(f'output{i}.txt')

    #import delresults
    #delresults.empty_csv_file("resultsFEDNIP.csv")
    removefilesnames.remove_client_files("client", num_clients)
    #RemoveGlobalweights.remove_file("weightsglobal.pth")
    import resettracklist
    resettracklist.reset_values_in_file("tracklist.json")
    setserverround.set_server_round()
    emptyLogSwaps.empty_log_swaps()
    print(server_round)
    print(globalvariables.warmup)
    print(globalvariables.strategy)
    if not globalvariables.warmup and globalvariables.strategy == "FedNIP":
        def evaluate(server_round1,parameters,config):
            server_round = getserverround.get_server_round('globalvariables.py')
            if server_round == 0:
                print("I came to here")
                return 0, {"accuracy": 0}
            if server_round > 0:
               print(f"warmupvariable {globalvariables.warmup} type is {type(globalvariables.warmup)}")

               if check_special_training(int(server_round)):
                    # Create a deepcopy of the model

                    #local_epochs = config[""]


                    from countmatchingfiles import read_matching_files
                    from ChooseClient import get_top_performers_and_random_clients
                    import os

                    def get_file_content(file):
                        with open(file, "r",encoding="utf-8") as f:
                            return f.read()

                    contents = read_matching_files()
                    for clientid, file_path in contents:
                        print(f"Client ID: {clientid}")
                        print(f"File Path: {file_path}")
                        globclientid = clientid
                        # Example usage
                        # Access the currentcluster variable
                        #current_cluster = globalvariables.currentcluster
                        from findclusterid import find_cluster_id

                        #net = Net().to(DEVICE)
                        net_copy = copy.deepcopy(globalnet)
                        set_parameters(net_copy, torch.load(file_path))  # Update model with the latest parameters
                        loss, accuracy = test(net_copy, testloader)

                        print(f"Accuracy updated for '{clientid}' in '{file_path}'.")

                        # Example usage
                        file_path1 = "top_performers.json"
                        file_path2 = "random_performers.json"
                        client_id = clientid
                        new_accuracy = accuracy
                        print(new_accuracy)

                        update_client_accuracy(file_path1, client_id, new_accuracy)
                        update_client_accuracy(file_path2, client_id, new_accuracy)

                        print(f"Proxy server-side evaluation loss {loss} / accuracy {accuracy}")
                        del net_copy

                    # you dont give k and r values here, because that happens in the selection
                    top_performers_file = 'top_performers.json'
                    random_performers_file = 'random_performers.json'
                    random_threshold = globalvariables.r  # Threshold for comparing random performers with top performers (in percentage)

                    updaterankings.update_rankings(top_performers_file, random_performers_file, 0, 0)
                    updatetracklist.update_tracklist_ranking()

                    bestfile_path = findbestfilepath.find_best_file_path()

                    set_parameters(globalnet, torch.load(bestfile_path))  # Update model with the best parameters
                    loss, accuracy = test(globalnet, testloader)
                    print(f"Server-side evaluation loss {loss} / accuracy {accuracy}")
                    removefilesnames.remove_client_files("client",num_clients)
                    RemoveGlobalweights.remove_file("weightsglobal.pth")
                    torch.save(get_parameters(globalnet), f"weightsglobal.pth")
                    #torch.save(globalnet.state_dict(), 'global_model.pth')
                    # proxy model prevents overfitting
                    import csv
                    filename = 'centraleval.csv'

                    # Function to write a single row of data to the CSV file
                    def write_row(data):
                        with open(filename, 'a', newline='') as file:  # Open the CSV file in append mode
                            writer = csv.writer(file)
                            writer.writerow(data)

                    data = [int(server_round), round(accuracy, 4)]
                    # Write the header row to the CSV file
                    write_row(data)

                    # Read the content of the file into a variable
                    with open('filenameserver.txt', 'r') as file:
                        filename= file.read()

                    resultsFEDNIP.write_to_csv(filename, server_round, round(accuracy, 4))
                    return loss, {"accuracy": accuracy}

               else:
                   print(server_round)
                   bestfile_path = findbestfilepath.find_best_file_path()
                   set_parameters(globalnet, torch.load(bestfile_path))  # Update model with the best parameters
                   loss, accuracy = test(globalnet, testloader)
                   print(f"Server-side evaluation loss NO SPECIAL TRAINING {loss} / accuracy {accuracy}")
                   removefilesnames.remove_client_files("weightsglobal.pth",num_clients)
                   torch.save(get_parameters(globalnet), f"weightsglobal.pth")
                   # Read the content of the file into a variable
                   with open('filenameserver.txt', 'r') as file:
                       filename = file.read()

                   resultsFEDNIP.write_to_csv(filename, server_round, round(accuracy, 4))
                   return loss, {"accuracy": accuracy}


        return evaluate

    else:
        def evaluate(server_round1, parameters, config):
            server_round = getserverround.get_server_round('globalvariables.py')
            print("WARMUP")
            return 0, {"accuracy": 0}
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