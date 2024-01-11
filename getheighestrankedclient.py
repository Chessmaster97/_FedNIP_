import json

def get_highest_ranked_client(cluster_id):
    # Step 1: Read the JSON file
    with open('tracklist.json', 'r') as file:
        tracklist = json.load(file)

    # Step 2: Find the cluster based on the given cluster ID
    cluster = next((c for c in tracklist['clusters'] if c['id'] == cluster_id), None)

    if cluster:
        # Step 3: Get the clients within the cluster
        clients = cluster['clients']

        if clients:
            # Step 4: Get the highest ranked client (first client in the list)
            highest_ranked_client = clients[0]

            return highest_ranked_client

    return None  # Cluster not found or no clients in the cluster

