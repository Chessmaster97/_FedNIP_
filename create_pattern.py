import json

training_data = [{"Round Number": i, "Label": "Special Training"} for i in range(0, 501)]

with open('pattern_data.json', 'w') as json_file:
    json.dump(training_data, json_file)
