import EMD_calculator
import buildtracklist
import os
import DataLoad
import globalvariables


def start_process():
    file_path = 'demofile2.txt'

    # Open the file in write mode, which will truncate its content
    with open(file_path, 'w') as file:
        pass

    i = 0
    while True:
        train_path = f'trainloader{i}.pth'
        val_path = f'valloader{i}.pth'

        if os.path.exists(train_path):
            os.remove(train_path)
        else:
            print(f'File not found: {train_path}. Reached the end.')
            break

        if os.path.exists(val_path):
            os.remove(val_path)
        else:
            print(f'File not found: {val_path}. Reached the end.')
            break

        i += 1

    DataLoad.callDataLoad()
    if not globalvariables.strategy == "FedAVG" or not globalvariables.strategy == "FedProx":
        EMD_calculator.calculateEMD()
        buildtracklist.process_csv_and_write_json()

# Call the function to start the process
start_process()
