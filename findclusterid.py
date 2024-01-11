import json

def find_cluster_id(client_id):
    # Step 1: Read the JSON file
    with open('tracklist.json', 'r') as file:
        tracklist = json.load(file)

    # Step 2: Iterate over clusters and find the one containing the client ID
    for cluster in tracklist['clusters']:
        if client_id in cluster['clients']:
            return cluster['id']

    return None  # Client ID not found in any cluster

# Example usage
#client_id = 2

#cluster_id = find_cluster_id(client_id)
#if cluster_id is not None:
    #print("Cluster ID for Client", client_id, ":", cluster_id)
#else:
    #print("Client", client_id, "not found in any cluster.")
