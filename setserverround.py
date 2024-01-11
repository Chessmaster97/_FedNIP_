def set_server_round():
    filename = 'globalvariables.py'

    with open(filename, 'r') as file:
        content = file.read()
        lines = content.split('\n')

    updated_lines = []
    for line in lines:
        if 'serverround =' in line:
            updated_lines.append('serverround = 0\n')
        else:
            updated_lines.append(line + '\n')

    with open(filename, 'w') as file:
        file.writelines(updated_lines)
set_server_round()