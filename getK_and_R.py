def get_K_and_R_from_config():
    with open('config.ini', 'r') as file:
        lines = file.readlines()

    K = None
    R = None

    for line in lines:
        line = line.strip()
        if line.startswith("K ="):
            K = float(line.split('=')[1].strip())
        elif line.startswith("R ="):
            R = float(line.split('=')[1].strip())

    return K, R

# Example usage
K_value, R_value = get_K_and_R_from_config()

print(f"K = {K_value}, R = {R_value}")
