import json
from globalvariables import num_rounds

num_communication_rounds = num_rounds

data = []
for round_num in range(1, num_communication_rounds + 1):
    if round_num % 3 == 1:
        label = "Special Training"
    else:
        label = "No Special Training"

    data.append({
        "Round Number": round_num,
        "Label": label
    })

file_path = "pattern_data.json"

# Write data to JSON file
with open(file_path, 'w') as file:
    json.dump(data, file, indent=4)
