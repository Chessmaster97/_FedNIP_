import json
import random
import math

import globalvariables


def select_clients(clusters, clients, k, r):
    # Select a cluster with the lowest chosen count
    target_cluster = min(clusters, key=lambda x: x['chosen_count'])
    globalvariables.currentcluster = target_cluster
    print(target_cluster)

    # Calculate the number of top performers to choose
    top_count = math.ceil(k * len(target_cluster['clients']))
    print(top_count)

    # Calculate the number of random clients to choose
    random_count = math.ceil(r * len(target_cluster['clients']))
    print(random_count)

    # Select top performers from the target cluster
    top_performers = target_cluster['clients'][:top_count]
    print(top_performers)

    # Select random clients from the target cluster excluding the top performers
    random_clients = random.sample(target_cluster['clients'][top_count:], random_count)

    # Update chosen count for the selected cluster
    target_cluster['chosen_count'] += 1

    # Update chosen count for the selected clients
    for client_id in top_performers + random_clients:
        clients[str(client_id)]['chosen_count'] += 1

    return target_cluster['id'], top_performers, random_clients

# Load data from the tracklist.json file
with open('tracklist.json') as file:
    data = json.load(file)

# Extract clusters and clients from the loaded data
clusters = data['clusters']
clients = data['clients']

# Example usage
k = 0.2
r = 0.6

cluster_id, top_performers, random_clients = select_clients(clusters, clients, k, r)
print("Cluster ID:", cluster_id)
print("Top Performers:", top_performers)
print("Random Clients:", random_clients)

# Update the tracklist.json file with the modified data
with open('tracklist.json', 'w') as file:
    json.dump(data, file, indent= 4)
"""

1. select clients for training. Pick from cluster clients that have lowest chosen round.
2. when local training has finished, send parameters to server and global model. 
3. At the global determine if we want to train with proxy model. 
 - if we want to train with the proxy model, we examine the weights of each client in the cluster on the copy of the global model. Based on this update ranking and use best weights
 - if we dont want to use the proxy model, pick the best weights of the cluster 

When to save the weights of the clients. Save at the end of the round and delete at the beginning of the round. can do in sample method. 

"""