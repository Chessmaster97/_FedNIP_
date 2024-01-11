import json
import math
import random

def get_top_performers_and_random_clients(tracklist_data, k, r, cluster_id):
    clusters = tracklist_data["clusters"]
    clients_data = tracklist_data["clients"]

    # Find the cluster with the given cluster_id
    cluster = next((c for c in clusters if c["id"] == cluster_id), None)
    if cluster is None:
        return [], []

    clients_in_cluster = cluster["clients"]
    chosen_count = cluster["chosen_count"]
    total_clients_in_cluster = len(clients_in_cluster)

    num_top_performers = math.ceil(k * total_clients_in_cluster)
    num_random_clients = math.ceil(r * total_clients_in_cluster)

    num_top_performers = min(num_top_performers, total_clients_in_cluster)
    num_random_clients = min(num_random_clients, total_clients_in_cluster - num_top_performers)

    print(f"random clients number: {num_random_clients}")

    # Sort clients in the cluster based on their performance (descending order)
    sorted_clients = sorted(clients_in_cluster, key=lambda c: clients_data[str(c)]["performance"], reverse=True)

    # Select the top performers from the sorted list
    top_performers = sorted_clients[:num_top_performers]

    # Select random clients from the remaining clients in the cluster
    remaining_clients = sorted_clients[num_top_performers:]
    random_clients = random.sample(remaining_clients, num_random_clients)

    return top_performers,random_clients

