import csv
import numpy as np
import pandas as pd
import seaborn as sns
from fitter import Fitter, get_common_distributions, get_distributions
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
# percentage samples in each category

dataset = pd.read_csv("./partition-reports/cifar10_hetero_dir_0.3_100clients12.csv")


print(dataset.T[1].values)
Svalues = []
for i in range(len(dataset.T[0].values)):
    if i > 0 and i is not len((dataset.T[0].values)) -1:
        Svalues.append(dataset.T[0].values[i])
print(Svalues)

import re

clientid = re.findall(r'\d+', dataset.T[0].values[0])[0]

print(clientid)

max_val = max(Svalues)
max_idx = Svalues.index(max_val)
print(max_idx)

import csv

header = ['Client id on client', 'Client id on server', 'Group']
data = [clientid,-1, max_idx]
with open('GroupClient.csv', 'w', encoding='UTF8') as f:
    # write the header
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerow(data)
    f.close()

# determine first most three values
# client 0: [class 2, class 3, class 4]
# client 0: [class 2, class 3, class 4]