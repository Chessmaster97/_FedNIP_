import csv
import json

def process_csv_and_write_json():
    # Initialize the data structure
    data = {
        "clusters": [],
        "clients": {}
    }

    # Read the CSV file and populate the data structure
    with open('client_clusters.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            client_id = int(row['Clientid'])
            group = int(row['Group'])

            # Update the clusters
            if group not in [cluster['id'] for cluster in data['clusters']]:
                data['clusters'].append({
                    'id': group,
                    'clients': [],
                    'chosen_count': 0
                })
            cluster_index = next(index for index, cluster in enumerate(data['clusters']) if cluster['id'] == group)
            data['clusters'][cluster_index]['clients'].append(client_id)

            # Update the clients
            data['clients'][client_id] = {
                'chosen_count': 0,
                'performance': []  # Initialize performance to 0
            }

    print(data)

    # Write the data structure to a JSON file
    with open('tracklist.json', 'w') as file:
        json.dump(data, file, indent=4)

