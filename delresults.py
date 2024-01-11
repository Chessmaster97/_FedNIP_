def empty_csv_file(csv_file_path):
    try:
        with open(csv_file_path, 'w', newline='') as csvfile:
            csvfile.truncate()
        print(f"The file '{csv_file_path}' has been emptied.")
    except FileNotFoundError:
        print(f"Error: The file '{csv_file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")