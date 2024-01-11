import json
import os

def generate_special_training(rounds):
    special_training_list = []
    for i in range(2, rounds+2):
        special_training_list.append({"Round Number": i, "Label": "Special Training"})
    return special_training_list

# Set dynamically how many round numbers with special training you want
num_rounds = 300

result = generate_special_training(num_rounds)

# Remove existing data from pattern_data.json
if os.path.exists('pattern_data.json'):
    os.remove('pattern_data.json')

# Write the output to a JSON file
with open('pattern_data.json', 'w') as json_file:
    json.dump(result, json_file)

print("Data written to pattern_data.json")
