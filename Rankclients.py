import json


def sort_clients_by_performance(cluster, client_data):
    clients = cluster['clients']
    return sorted(clients, key=lambda client_id: client_data[str(client_id)]['performance'][0], reverse=True)


def update_cluster_rankings(tracklist_file):
    # Read tracklist data from file
    with open(tracklist_file, 'r') as file:
        data = json.load(file)

    client_data = data['clients']

    # Iterate through clusters
    for cluster in data['clusters']:
        sorted_clients = sort_clients_by_performance(cluster, client_data)
        cluster['clients'] = sorted_clients

    # Write updated data back to file
    with open(tracklist_file, 'w') as file:
        json.dump(data, file, indent=4)


# Example Usage
update_cluster_rankings('tracklist.json')
