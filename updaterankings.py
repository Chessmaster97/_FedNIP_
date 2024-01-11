import json

def update_rankings(top_performers_file, random_performers_file, top_threshold, random_threshold):
    swap_log = []
    # Step 1: Read the top performers file
    with open(top_performers_file, 'r') as file:
        top_performers = json.load(file)

    # Step 2: Read the random performers file
    with open(random_performers_file, 'r') as file:
        random_performers = json.load(file)

    # Step 3: Sort random performers based on accuracy (highest to lowest)
    random_performers.sort(key=lambda x: x['accuracy'], reverse=True)

    # Step 4: Sort top performers based on accuracy (highest to lowest)
    top_performers.sort(key=lambda x: x['accuracy'], reverse=True)

    # Step 5: Compare and swap top performers based on the top threshold
    for i, random_client in enumerate(random_performers):
        for j, top_client in enumerate(top_performers):
            if random_client['accuracy'] > top_client['accuracy'] + top_threshold:
                swap_log.append({
                    'top_client_id': top_client['clientID'],
                    'random_client_id': random_client['clientID'],
                    'top_accuracy': top_client['accuracy'],
                    'random_accuracy': random_client['accuracy'],
                    'random_threshold': random_threshold,
                    'threshold_dif': round(random_client['accuracy'] - top_client['accuracy'], 4)
                })
                random_performers[i], top_performers[j] = top_performers[j], random_performers[i]
                break

    # Step 6: Write the updated rankings back to the files
    with open(top_performers_file, 'w') as file:
        json.dump(top_performers, file, indent=4)

    with open(random_performers_file, 'w') as file:
        json.dump(random_performers, file, indent=4)

    # Write swap log to the log_file
    with open("LogSwaps.json", 'a') as log_file:
        for swap_info in swap_log:
            log_file.write(json.dumps(swap_info) + '\n')

