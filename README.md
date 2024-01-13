# FedNIP: A Statistical Heterogeneity Aware Dynamic Ranking Algorithm for Federated Learning
Code for paper - **[Federated Learning on Non-IID Data with Local-drift Decoupling and Correction]**

We provide code to run FedDC, FedAvg, 
[FedDyn](https://openreview.net/pdf?id=B7v4QMR6Z9w), 
[Scaffold](https://openreview.net/pdf?id=B7v4QMR6Z9w), and [FedProx](https://arxiv.org/abs/1812.06127) methods.


## Prerequisite
* Install the libraries listed in requirements.txt
    ```
    pip install -r requirements.txt
    ```

  
## Config file
In the config file all the important parameters can be set. The run file uses this file to set the parameters:


| Parameter      | Description                                                                                    |
| --------------- | ---------------------------------------------------------------------------------------------- |
| `Strategy`         | The strategy selected for training. Options: `FedProx`, `FedNIP`, `FedAvg`.        |
| `Num_Clients`       | Number of clients you want for the simulation. Give an integer as input . |
| `Num_Rounds`           | Number of rounds in simulation. Give an integer as input. |
| `Dir_parameter`            |                                          |
| `K`    | Batch size, default = `64`.                                                                    |
| `R`        | Number of local training epochs, default = `5`.                                                |
| `P`     | Number of parties, default = `2`.                                                              |
| `T`            | The proximal term parameter for FedProx, default = `0.001`.                                    |
| `Mu`           | The parameter controlling the momentum SGD, default = `0`.                                    |
| `Evaluationinterval`    | Number of communication rounds to use, default = `50`.                                         |
| `L`    | Learning rate for the local models, default = `0.01`. .                                         |
| `E`     | The partition way. Options: `homo`, `noniid-labeldir`, `noniid-#label1` (or 2, 3, ..., which means the fixed number of labels each party owns), `real`, `iid-diff-quantity`. Default = `homo`. |

## Running experiments

1. Run the following script to run experiments on the MNIST dataset for all above methods:
    ```
    python run.py
    ```

