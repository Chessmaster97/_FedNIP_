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

dir_parameters = [0.3]
num_clients = [250]
algorithms = ["FedNIP_full","FedNIP_part"]

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
