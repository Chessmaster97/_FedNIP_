import json

import globalvariables


def reset_values_in_file(file_path):
    globalvariables.currentcluster = 0
    # Read data from tracklist.json
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Reset chosen_count for clusters
    for cluster in data['clusters']:
        cluster['chosen_count'] = 0

    # Reset chosen_count and performance for clients
    for client in data['clients']:
        data['clients'][client]['chosen_count'] = 0

        # Check if performance is not an empty list
        if data['clients'][client]['performance']:
            data['clients'][client]['performance'][0] = 0.0
        else:
            data['clients'][client]['performance'] = [0.0]

    # Write the modified data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
