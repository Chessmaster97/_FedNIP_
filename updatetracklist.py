import json

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def find_cluster_with_top_performers(tracklist_data, top_performers):
    for cluster in tracklist_data['clusters']:
        if any(client in cluster['clients'] for client in top_performers):
            return cluster

def update_cluster_ranking(cluster, performer_ranking):
    cluster['clients'].sort(key=lambda x: performer_ranking.get(x, float('inf')))

def update_tracklist_ranking():
    tracklist_data = read_json('tracklist.json')
    top_performer_data = read_json('top_performers.json')
    top_performers = [performer['clientID'] for performer in top_performer_data]

    cluster = find_cluster_with_top_performers(tracklist_data, top_performers)
    if cluster:
        performer_ranking = {client: position for position, client in enumerate(top_performers)}
        update_cluster_ranking(cluster, performer_ranking)

    write_json('tracklist.json', tracklist_data)
