import os
import re

import getclusterid
import globalvariables
import json

def get_clients_in_current_cluster(file_path, current_cluster):
    with open(file_path, 'r') as file:
        data = json.load(file)
        clusters = data.get('clusters', [])
        clients_data = data.get('clients', {})

        for cluster in clusters:
            if cluster.get('id') == current_cluster:
                print("I am in the matchingfiles: Cluster ID:", current_cluster)
                print("Cluster Clients:", cluster.get("id"))
                client_ids = cluster.get('clients', [])
                clients_in_cluster = []
                for client_id in client_ids:
                    client_info = clients_data.get(str(client_id), {})
                    clients_in_cluster.append({
                        'client_id': client_id
                    })
                return clients_in_cluster

    return []

def read_matching_files():
    file_pattern = r"client(\d+)_data\.pth"
    matching_files = [filename for filename in os.listdir(".") if re.match(file_pattern, filename)]
    file_contents = []

    for file in matching_files:
        clientid = re.search(r"client(\d+)", file).group(1)
        file_path = os.path.abspath(file)
        with open(file_path, "r") as f:
            file_contents.append((clientid, file_path))

    # Use get_clients_in_current_cluster function to filter file_contents
    file_path = 'tracklist.json'
    current_cluster = getclusterid.get_current_cluster()
    clients_in_cluster = get_clients_in_current_cluster(file_path, current_cluster)

    filtered_contents = []

    for client_info in clients_in_cluster:
        client_id = client_info['client_id']
        for clientid, file_path in file_contents:
            if int(client_id) == int(clientid):
                filtered_contents.append((clientid, file_path))

    return filtered_contents

# Call the function
result = read_matching_files()
print(result)

# Print the result
for client_id, file_path in result:
    print(f"Client ID: {client_id}, File Path: {file_path}")