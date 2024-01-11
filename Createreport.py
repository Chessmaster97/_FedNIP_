import data as data
import torch
import torchvision
import torchvision.transforms as transforms
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from fedlab.utils.dataset.partition import CIFAR10Partitioner
from fedlab.utils.functional import partition_report
from torch.utils.data import DataLoader, random_split
from torchvision import datasets

csv_file = "./partition-reports/cifar10_hetero_dir_0.3_100clients.csv"
def create_parts(trainset,train_part, num_classes):
    partition_report(trainset.targets, train_part.client_dict,
                 class_num=num_classes,
                 verbose=False, file=csv_file)

hetero_dir_part_df = pd.read_csv(csv_file,header=1)
hetero_dir_part_df = hetero_dir_part_df.set_index('client')
col_names = [f"class{i}" for i in range(num_classes)]
for col in col_names:
    hetero_dir_part_df[col] = (hetero_dir_part_df[col] * hetero_dir_part_df['Amount']).astype(int)


with open("./partition-reports/cifar10_hetero_dir_0.3_100clients.csv",'r') as f:
    with open("./partition-reports/cifar10_hetero_dir_0.3_100clients12.csv",'w') as f1:
        next(f) # skip header line
        for line in f:
            f1.write(line)

dataset = pd.read_csv("./partition-reports/cifar10_hetero_dir_0.3_100clients12.csv")

hetero_dir_part_df[col_names].iloc[:20].plot.barh(stacked=True)
plt.tight_layout()
plt.xlabel('sample num')
plt.savefig(f"./img/cifar10_hetero_dir_0.3_100clientsr.png", dpi=400)

