from collections import OrderedDict
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, random_split
from torchvision.datasets import CIFAR10

import flwr as fl

DEVICE = torch.device("cpu")  # Try "cuda" to train on GPU
print(
    f"Training on {DEVICE} using PyTorch {torch.__version__} and Flower {fl.__version__}"
)

transform = transforms.Compose(
    [transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
)
trainset = torchvision.datasets.CIFAR10(root="../../../../data/CIFAR10/",
                                        train=True, download=True, transform=transform)
testset = torchvision.datasets.CIFAR10(root="../../../../data/CIFAR10/",
                                       train=False, download=True, transform = transform)

testloader = DataLoader(testset, batch_size=32, num_workers=0, shuffle=True)
valloader_global = DataLoader(trainset, batch_size=32, num_workers=0, shuffle=True)