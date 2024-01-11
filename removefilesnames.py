import os

def remove_client_files(file_namestart, num_iterations):
    i = 0

    for _ in range(num_iterations):
        file_name = f"{file_namestart}{i}_data.pth"

        if os.path.exists(file_name):
            os.remove(file_name)
            #print(f"Removed {file_name}")

        i += 1

# Example usage: Remove files with prefix "client" for 5 iterations
remove_client_files("client", 250)

