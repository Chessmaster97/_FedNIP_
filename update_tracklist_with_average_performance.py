import json
import os

def compute_average_accuracy(client_id):
    file_path = "valid_json_file1.json"
    if not os.path.exists(file_path):
        return None

    total_accuracy = 0.0
    count = 0
    with open(file_path, "r") as file:
        for line in file:
            data = json.loads(line)
            accuracy = data.get("accuracy")
            if accuracy is not None:
                total_accuracy += accuracy
                count += 1

    if count == 0:
        return None

    average_accuracy = total_accuracy / count
    print(average_accuracy)
    return average_accuracy


def update_tracklist():
    with open("tracklist.json", "r") as file:
        tracklist = json.load(file)

    clients = tracklist["clients"]

    for client_id in clients:
        average_accuracy = compute_average_accuracy(client_id)
        if average_accuracy is not None:
            clients[client_id]["performance"].append(average_accuracy)

    sorted_clients = sorted(clients.items(), key=lambda x: sum(x[1]["performance"]), reverse=True)
    clusters = tracklist["clusters"]

    for i, (_, client_data) in enumerate(sorted_clients):
        clusters[i]["clients"] = [int(client_id) for client_id in client_data["performance"]]

    with open("tracklist.json", "w") as file:
        json.dump(tracklist, file, indent=4)


# Example usage
update_tracklist()
