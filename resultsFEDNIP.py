import csv

def write_to_csv(filename, round_num, accuracy):
    data = {
        'communication round': round_num,
        'accuracy': accuracy
    }

    with open(filename, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if file.tell() == 0:
            writer.writeheader()  # Write header only if the file is empty
        writer.writerow(data)
