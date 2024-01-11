import json

def check_special_training(current_round):
    file_path = "pattern_data.json"

    # Read the JSON file
    with open(file_path, 'r') as file:
        pattern_data = json.load(file)

    # Iterate over each entry in the pattern data
    for entry in pattern_data:
        round_number = entry["Round Number"]
        label = entry["Label"]

        # Check if the current round matches the round number in the JSON file
        if current_round == round_number:
            if label == "Special Training":
                return True

    return False
