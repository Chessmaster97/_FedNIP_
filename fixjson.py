import json
import os

def process_output_files():
    output_files = [file for file in os.listdir('.') if file.startswith('output') and file.endswith('.txt')]
    count = len(output_files)

    print(f"The number of output files is: {count}")

    for i in range(count):
        client_list = []

        with open(f'output{i}.txt') as f:
            for json_obj in f:
                client_dict = json.loads(json_obj)
                client_list.append(client_dict)

        print(json.dumps(client_list))

        valid_json = json.dumps(client_list)
        f = open(f"goodoutput{i}.json", "w")
        f.write(valid_json)
        f.close()

# Call the function to execute the code
process_output_files()
