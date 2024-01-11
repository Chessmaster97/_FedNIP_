import json
import random

# Load the JSON file
with open("data.json", "r") as file:
    data = json.load(file)

# Retrieve the clusters and clients data from the JSON
clusters = data["clusters"]
clients = data["clients"]

# Helper function to get the next client ID based on chosen_count
def get_next_client_id(cluster):
    clients_in_cluster = cluster["clients"]
    chosen_count = cluster["chosen_count"]
    client_id = clients_in_cluster[chosen_count % len(clients_in_cluster)]
    chosen_count += 1
    cluster["chosen_count"] = chosen_count
    return client_id

# Visit all clients in each cluster if they haven't been chosen yet
for cluster in clusters:
    clients_in_cluster = cluster["clients"]
    for client_id in clients_in_cluster:
        client = clients[str(client_id)]
        if client["chosen_count"] == 0:
            # Simulate neural network performance (accuracy)
            performance = random.uniform(0.7, 0.9)  # Replace with your neural network evaluation code

            # Update the client's performance
            client["performance"] = performance
            client["chosen_count"] = 1

# Sort clients within each cluster based on performance
for cluster in clusters:
    clients_in_cluster = cluster["clients"]
    sorted_clients = sorted(clients_in_cluster, key=lambda client_id: clients[str(client_id)]["performance"], reverse=True)
    cluster["clients"] = sorted_clients

# Print the updated data with rankings
print(json.dumps(data, indent=4))
