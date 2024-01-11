def read_configuration_variables():
    file_path = 'config.ini'
    config_values = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line and '=' in line and not line.startswith(';'):
                key, value = line.split('=')
                config_values[key.strip()] = value.strip()

    # Extract the variables of interest
    strategy = config_values.get('Strategy', '')
    dir_parameter = float(config_values.get('Dir_parameter', 0))
    e = int(config_values.get('E', 1))
    num_clients = int(config_values.get('Num_Clients', 0))
    k = float(config_values.get('K', 0))
    r = float(config_values.get('R', 0))
    t = float(config_values.get('T', 0))

    return strategy, dir_parameter, e, num_clients, k, r, t

strategy, dir_parameter, e, num_clients, k, r, t = read_configuration_variables()
print(f"Strategy: {strategy}")
print(f"Dir_parameter: {dir_parameter}")
print(f"E: {e}")
print(f"Num_Clients: {num_clients}")
print(f"K: {k}")
print(f"R: {r}")
print(f"T: {t}")


