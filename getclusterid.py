def get_current_cluster():
    with open('globalvariables.py', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if 'currentcluster =' in line:
                current_cluster = int(line.split('=')[1].strip())
                return current_cluster
    # If 'currentcluster' is not found, you can return a default value or raise an exception
    return None
