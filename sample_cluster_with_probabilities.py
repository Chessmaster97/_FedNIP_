import random
import json

def sample_cluster_with_probabilities():
    # Load the JSON data
    with open('tracklist.json', 'r') as json_file:
        data = json.load(json_file)

    # Get cluster data and cluster counts from the loaded data
    cluster_data = {cluster['id']: cluster['clients'] for cluster in data['clusters']}
    total_clients = sum(len(clients) for clients in cluster_data.values())

    probabilities = {cluster_id: len(clients) / total_clients for cluster_id, clients in cluster_data.items()}

    chosen_cluster_id = random.choices(list(probabilities.keys()), list(probabilities.values()))[0]

    # Get the clients that belong to the chosen cluster
    chosen_cluster_clients = cluster_data[chosen_cluster_id]

    # Update the chosen count for the selected cluster
    selected_cluster = next((cluster for cluster in data['clusters'] if cluster['id'] == chosen_cluster_id), None)
    if selected_cluster is not None:
        selected_cluster['chosen_count'] += 1

    # Save the updated data back to tracklist.json file
    with open('tracklist.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)

    return chosen_cluster_id, chosen_cluster_clients
