import torch
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, random_split
from torchvision.datasets import CIFAR10


def load_datasets(num_clients: int):
    # Download and transform CIFAR-10 (train and test)
    transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
    )
    trainset = CIFAR10("./dataset", train=True, download=True, transform = transform)
    #print(len(trainset))
    testset = CIFAR10("./dataset", train=False, download=True, transform=transform)
    #print(len(testset))

    # Split training set into `num_clients` partitions to simulate different local datasets
    partition_size = len(trainset) // num_clients
    lengths = [partition_size] * num_clients
    datasets = random_split(trainset, lengths, torch.Generator().manual_seed(42))
    #print(trainset)

     # Split each partition into train/val and create DataLoader
    trainloaders = []
    valloaders = []
    for ds in datasets:
        len_val = len(ds) // 10  # 10 % validation set
        len_train = len(ds) - len_val
        lengths = [len_train, len_val]
        ds_train, ds_val = random_split(ds, lengths, torch.Generator().manual_seed(42))
        #print(ds_train)
        #print(ds_train,ds_val)
        trainloaders.append(DataLoader(ds_train, batch_size=32, shuffle=True))
        valloaders.append(DataLoader(ds_val, batch_size=32))
    testloader = DataLoader(testset, batch_size=32)
    print(len(valloaders))
    print(len(trainloaders))
    print(valloaders[0])
    print(trainloaders[0])

    print(next(iter(valloaders[0])))
    print(next(iter(trainloaders[0])))

    #print(trainloaders, valloaders, testloader)
    #for batch_idx, target in enumerate(trainloaders):
        #print(target)
    return trainloaders, valloaders, testloader

load_datasets(10)