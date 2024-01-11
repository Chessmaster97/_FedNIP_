import json

# Load tracklist.json
with open('tracklist.json', 'r') as file:
    tracklist = json.load(file)

# Iterate over clients
for client_id in tracklist['clients']:
    # Load goodoutput.json for the client
    filename = f'goodoutput{client_id}.json'
    with open(filename, 'r') as file:
        goodoutput = json.load(file)

    # Exclude first round accuracy
    goodoutput = goodoutput[1:]

    # Compute average accuracy for the client
    accuracies = [entry['accuracy'] for entry in goodoutput if entry['accuracy'] is not None]
    if len(accuracies) > 0:
        average_accuracy = sum(accuracies) / len(accuracies)
    else:
        average_accuracy = 0.0

    average_accuracy = round(average_accuracy, 4)
    # Update performance in tracklist.json
    tracklist['clients'][str(client_id)]['performance'] = [average_accuracy]

# Save updated tracklist.json
with open('tracklist.json', 'w') as file:
    json.dump(tracklist, file, indent=4)
