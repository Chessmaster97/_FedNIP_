def get_server_round(filename):
    with open(filename, 'r') as file:
        content = file.read()
        lines = content.split('\n')
        for line in lines:
            if 'serverround =' in line:
                server_round = int(line.split('=')[1].strip())
                return server_round
