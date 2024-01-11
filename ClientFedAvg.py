from collections import OrderedDict
import time
from collections import OrderedDict
from typing import List

from numpy.ma import copy

import CheckStrategy
import DataLoad
import flwr as fl
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import NeuralNet
import clientperformance
import getserverround
import globalvariables
import resultsFEDNIP
import warmupclients



DEVICE = torch.device("cpu")

class Net(nn.Module):
    def __init__(self) -> None:
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def get_parameters(net) -> List[np.ndarray]:
    return [val.cpu().numpy() for _, val in net.state_dict().items()]


def set_parameters(net, parameters: List[np.ndarray]):
    params_dict = zip(net.state_dict().keys(), parameters)
    state_dict = OrderedDict({k: torch.Tensor(v) for k, v in params_dict})
    net.load_state_dict(state_dict, strict=False)


def train(net, trainloader, epochs: int):
    """Train the network on the training set."""
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(net.parameters())
    net.train()
    for epoch in range(epochs):
        correct, total, epoch_loss = 0, 0, 0.0
        for images, labels in trainloader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            optimizer.zero_grad()
            outputs = net(images)
            #global_params = net.parameters()
            #proximal_term = 0
            #for local_weights, global_weights in zip(net.parameters(), global_params):
                #proximal_term += (local_weights - global_weights).norm(2)
            #loss = criterion(net(images), labels) + (0.001 / 2) * proximal_term
            loss = criterion(net(images), labels)
            loss.backward()
            optimizer.step()
            # Metrics
            epoch_loss += loss
            total += labels.size(0)
            correct += (torch.max(outputs.data, 1)[1] == labels).sum().item()
        epoch_loss /= len(trainloader.dataset)
        epoch_acc = correct / total

        with open('readme.txt', 'a') as f:
            f.write(f'readme {epoch_acc}')

        print(f"Epoch {epoch+1}: train loss {epoch_loss}, accuracy {epoch_acc}")

def test(net, valloader):
    """Evaluate the network on the entire test set."""
    criterion = torch.nn.CrossEntropyLoss()
    correct, total, loss = 0, 0, 0.0
    net.eval()
    with torch.no_grad():
        for images, labels in valloader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            outputs = net(images)
            loss += criterion(outputs, labels).item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    loss /= len(valloader.dataset)
    accuracy = correct / total

    return loss, accuracy

class FlowerClient(fl.client.NumPyClient):

    def __init__(self, cid, net, trainloader, valloader):
        self.cid = cid
        self.net = net
        self.trainloader = trainloader
        self.valloader = valloader

    def get_properties(self, config):
        properties = {"battery_level": 1.0}
        return properties

    def get_parameters(self, config):
        print(f"[Client {self.cid}] get_parameters")
        return get_parameters(self.net)

    def fit(self, parameters, config):
        # Read values from config
        self.server_round = config["server_round"]
        local_epochs = 1

        if self.server_round == 0:
            return [], 0, {"clientid": self.cid}
        print(f"[Client {self.cid}] fit, config: {config}")
        #set_parameters(self.net, parameters)

        if self.server_round > 0:
            set_parameters((self.net), torch.load("weightsglobalFedAvg.pth"))
            print("I used the weights of the global model")
        else:
            set_parameters(self.net, parameters)
            print("I did not use the weights of the global model")
        # Load the weights from globalweights_data.pth
        #global_weights = torch.load("globalweights_data.pth")
        # Assuming globalnet is available in this script
        #set_parameters(globalnet, global_weights)
        # Load the state of the global model
        #globalnet.load_state_dict(torch.load('global_model.pth'))

        # Assuming globalnet is available in this script
        #set_parameters(globalnet, get_parameters(globalnet))


        start = time.time()
        train(self.net, self.trainloader, epochs=local_epochs)
        stop = time.time()

        torch.save(get_parameters(self.net), f"client{int(self.cid)}_data.pth")
        return get_parameters(self.net), len(self.trainloader), {}

    def evaluate(self, parameters, config):
        #if self.server_round == 1:
            #return
        #print(f"[Client {self.cid}] evaluate, config: {config}")

        #set_parameters(self.net, parameters)
        set_parameters((self.net), torch.load("weightsglobalFedAvg.pth"))
        loss, accuracy = test(self.net, self.valloader)

        filename = f'Client_{self.cid}_FedAvg_nrc_10.csv'
        resultsFEDNIP.write_to_csv(filename,getserverround.get_server_round('globalvariables.py'),round(accuracy, 4))

        return float(loss), len(self.valloader), {"accuracy": float(accuracy)}

def client_fn1(cid) -> FlowerClient:
    net = Net().to(DEVICE)
    trainloader = torch.load(f'trainloader{int(cid)}.pth')
    valloader = torch.load(f'valloader{int(cid)}.pth')

    return FlowerClient(cid, net, trainloader, valloader)