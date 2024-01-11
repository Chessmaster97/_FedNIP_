import json

data = [{"Round Number": i, "Label": "Special Training"} for i in range(1001)]

with open('pattern_data.json', 'w') as file:
    json.dump(data, file, indent=2)
