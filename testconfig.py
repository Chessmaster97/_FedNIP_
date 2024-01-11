def update_config(strategy=None, num_clients=None, dir_parameter=None, k=None, r=None):
    # Read the existing config.ini file
    with open('config.ini', 'r') as file:
        lines = file.readlines()

    # Define the new values
    new_values = {
        'Strategy': strategy,
        'Num_Clients': num_clients,
        'Dir_parameter': dir_parameter,
        'K': k,
        'R': r
    }

    # Update the specific lines
    for i, line in enumerate(lines):
        for key, value in new_values.items():
            if key in line and value is not None:
                # Split the line at '=' to update only the value part
                key_value_pair = line.split('=')
                if len(key_value_pair) == 2 and key_value_pair[0].strip() == key:
                    lines[i] = f"{key} = {value}\n"
                    break

    # Write the changes back to the config.ini file
    with open('config.ini', 'w') as file:
        file.writelines(lines)

