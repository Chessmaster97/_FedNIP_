# FedNIP: A Statistical Heterogeneity Aware Dynamic Ranking Algorithm for Federated Learning
This is the code used for the implementation of FedNIP full, FedNIP part, FedAvg and FedProx. 

[FedNIP](https://openreview.net/pdf?id=B7v4QMR6Z9w), 
[FedAvg]([https://openreview.net/pdf?id=B7v4QMR6Z9w](https://openreview.net/pdf?id=eoQBpdMy81m#:~:text=The%20Federated%20Averaging%20(FedAvg)%20(,originally%20proposed%20through%20empirical%20observations.)), and [FedProx](https://arxiv.org/abs/1812.06127) methods.


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
2 In the run.py file you can set the parameters you want for the experiment in the lists below:

    dir_parameters = [0.6,0.3,0.05]
    num_clients = [50,100,250]
    algorithms = ["FedAvg","FedProx","FedNIP_full","FedNIP_part"]
    
    for dir_param in dir_parameters:
        for clients in num_clients:
            for algorithm in algorithms:
    
                print(dir_param, clients, algorithm)
                # Run initial setup for each parameter combination
    
                if algorithm == "FedNIP_full":
                    with open('filenameserver.txt', 'w') as file:
                        file.write(f"FINALRESULTS_{algorithm}_K=1_R=0_Clients_{clients}_DIR_{dir_param}_newrun.csv")
                    testconfig.update_config(strategy="FedNIP", num_clients=clients, dir_parameter=dir_param, k=1, r=0)
                    run_initial_setup()
                    server_command = "python ServerFedNip.py"
                    server_execution_time = execute_server(server_command)
                    write_execution_time(algorithm, clients, dir_param, server_execution_time)
                elif algorithm == "FedNIP_part":
                    with open('filenameserver.txt', 'w') as file:
                        file.write(f"FINALRESULTS_{algorithm}_K=0.1_R=0.1_Clients_{clients}_DIR_{dir_param}_newrun.csv")
                    testconfig.update_config(strategy="FedNIP", num_clients=clients, dir_parameter=dir_param, k=0.1, r=0.1)
                    run_initial_setup()
                    server_command = "python ServerFedNip.py"
                    server_execution_time = execute_server(server_command)
                    write_execution_time(algorithm, clients, dir_param, server_execution_time)
                elif algorithm == "FedAvg":
                    with open('filenameserver.txt', 'w') as file:
                        file.write(f"FINALRESULTS_{algorithm}_Clients_{clients}_{dir_param}.csv")
                    testconfig.update_config(strategy=algorithm, num_clients=clients, dir_parameter=dir_param, k=None, r=None)
                    run_initial_setup()
                    server_command = "python ServerFedAvg.py"
                    server_execution_time = execute_server(server_command)
                    write_execution_time(algorithm, clients, dir_param, server_execution_time)
                elif algorithm == "FedProx":
                    with open('filenameserver.txt', 'w') as file:
                        file.write(f"FINALRESULTS_{algorithm}_Clients_{clients}_{dir_param}.csv")
                    testconfig.update_config(strategy=algorithm, num_clients=clients, dir_parameter=dir_param, k=None, r=None)
                    run_initial_setup()
                    server_command = "python ServerFedProx.py"
                    server_execution_time = execute_server(server_command)
                    write_execution_time(algorithm, clients, dir_param, server_execution_time)
            ```
