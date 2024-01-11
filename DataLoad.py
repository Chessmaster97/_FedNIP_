
import torch
import torchvision
import torchvision.transforms as transforms
from fedlab.utils.dataset.partition import CIFAR10Partitioner
from fedlab.utils.functional import partition_report
from torch.utils.data import DataLoader, random_split
import os

import globalvariables
import removecsvheader
from globalvariables import num_clients


def loaddata(numclients: int):
    import torch.utils.data as data
    num_clients = numclients
    num_classes = 10
    seed = 2021
    Batchsize = 32
    hist_color = '#4169E1'

    transform = transforms.Compose(
            [transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
        )
    trainset = torchvision.datasets.CIFAR10(root="../../../../data/CIFAR10/",
                                            train=True, download=True, transform=transform)
    testset = torchvision.datasets.CIFAR10(root="../../../../data/CIFAR10/",
                                            train=False, download=True, transform=transform)

    # Split training set into 10 partitions to simulate the individual dataset
    partition_size = len(trainset) // numclients
    lengths = [partition_size] * numclients
    datasets = random_split(trainset, lengths, torch.Generator().manual_seed(42))

    # Split each partition into train/val and create DataLoader
    trainloaders = []
    valloaders = []
    for ds in datasets:
        len_val = len(ds) // 10  # 10 % validation set
        len_train = len(ds) - len_val
        lengths = [len_train, len_val]
        ds_train, ds_val = random_split(ds, lengths, torch.Generator().manual_seed(42))
        trainloaders.append(DataLoader(ds_train, batch_size=1, shuffle=True))
        valloaders.append(DataLoader(ds_val, batch_size=32))

    testloader = DataLoader(testset, batch_size=32, num_workers=0, shuffle=True)

    # After
    print('Train data set:', int(len(trainset) * 0.9))
    print('Val data set:', int(len(trainset) * 0.1))
    print('Test data set:', len(testset))

    def pardata(set,name):

        setloader = []
        settargets = []
        for i in range(len(trainloaders)):
            for batch_idx, (data, target) in enumerate(set[i]):
                settargets.append(target.item())

        #print(trainset[0])
        train_part = CIFAR10Partitioner(settargets,
                                             num_clients,
                                             balance=None,
                                             partition="dirichlet",
                                             dir_alpha=globalvariables.dir_parameter,
                                             seed=seed)

        #print(train_part.client_dict)
        csv_file = f"./partition-reports/clientsplit{name}.csv"
        partition_report(trainset.targets, train_part.client_dict,
                         class_num=num_classes,
                         verbose=False, file=csv_file)

        removecsvheader.remove_header('./partition-reports/clientsplittrain.csv', './partition-reports/clientsplittrain___.csv')

        def get_dataloader(data):
            batch_size = 32
            num_workers = 2
            #print(data)
            set_loader = DataLoader(data,
                                      shuffle=True,
                                      batch_size=batch_size,
                                      drop_last=True,
                                      num_workers=0)

            return set_loader

        #print(train_part.client_dict.keys())
        #print(train_part.client_dict.values())

        # using dict with key and indice of dataset of FedLab library
        for key, value in train_part.client_dict.items():
            data = torch.utils.data.Subset(trainset, value)
            setloader.append(get_dataloader(data))
            print(len(setloader))
        print(setloader)
        return setloader

    trainloaders1 = pardata(trainloaders,"train")
    #valloaders1 = pardata(valloaders,"val")
    #testloaders = pardata(testloader,"test")

    return trainloaders1,valloaders, testloader

file_path = 'demofile2.txt'
import pickle
def callDataLoad():
    if os.stat(file_path).st_size != 0:
        print("Data is already loaded")
        return
    else:
        trainloaders1, valloaders1, testloader1 = loaddata(num_clients)
        for i in range(0,num_clients):


            torch.save(trainloaders1[i], f'trainloader{i}.pth')
            torch.save(valloaders1[i], f'valloader{i}.pth')
        torch.save(testloader1, f'testloader.pth')
        f = open(file_path, 'w+')  # open file in write mode
        f.write('Data loaded')
        f.close()
        return

