import os

def remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        print(f"Removed {file_name}")
    else:
        print(f"{file_name} does not exist.")