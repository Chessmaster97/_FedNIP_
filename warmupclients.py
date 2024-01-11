import json

def create_data(cid, communication_round, epoch):
    data = {
        "client_id": cid,
        "communication_round": communication_round,
        "epoch": epoch,
        "accuracy": None
    }
    return data

def write_data_to_json(data, file_path):
    with open(file_path, "a") as file:
        json.dump(data, file)
        file.write('\n')

def update_accuracy(accuracy, file_path):
    updated_data = []
    with open(file_path, "r") as file:
        for line in file:
            data = json.loads(line)
            if data["accuracy"] is None:
                data["accuracy"] = round(accuracy,4)
            updated_data.append(data)

    with open(file_path, "w") as file:
        for data in updated_data:
            json.dump(data, file)
            file.write('\n')

