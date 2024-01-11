import json

# Function 1
def update_server_round(file_path, new_round):
    # Read the JSON file and load its contents into a dictionary
    with open(file_path, "r") as file:
        data = json.load(file)

    # Update the server_round value
    data["communication_round"] = new_round

    # Write the modified dictionary back to the JSON file
    with open(file_path, "w") as file:
        json.dump(data, file)

# Function 2
def update_client_id_and_accuracy(file_path, new_cid, new_accuracy):
    # Read the JSON file and load its contents into a dictionary
    with open(file_path, "r") as file:
        data = json.load(file)

    # Update the client_id and accuracy values
    data["client_id"] = new_cid
    data["accuracy"] = new_accuracy

    # Write the modified dictionary back to the JSON file
    with open(file_path, "w") as file:
        json.dump(data, file)
