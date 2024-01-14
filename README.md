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
2 The run.py look as follows:
    ```
    import subprocess
    import sys
    import time
    import testconfig
    
    def run_initial_setup():
        # Call the function from setupdata4.py using subprocess
        subprocess.run([sys.executable, "SetupData4.py"])
        # Add any additional setup steps here if needed
    
    def execute_server(server_command):
        server_start_time = time.time()
        server_process = subprocess.Popen(server_command, shell=True)
        while True:
            if server_process.poll() is not None:
                break
            time.sleep(1)
        server_end_time = time.time()
        return server_end_time - server_start_time
    
    def write_execution_time(algorithm, clients, dir_param, server_execution_time):
        filename = f"FINALEXECUTIONTIME_{algorithm}_{clients}_{dir_param}.txt"
        with open(filename, "w") as file:
            file.write(f"Total execution time: {server_execution_time:.2f} seconds\n")
    
    **dir_parameters = [0.3]
    num_clients = [250]
    algorithms = ["FedNIP_full","FedNIP_part"]**
    
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
