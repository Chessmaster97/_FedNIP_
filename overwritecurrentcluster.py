import fileinput

def overwrite_current_cluster(filename, new_cluster):
    with fileinput.FileInput(filename, inplace=True) as file:
        for line in file:
            if line.startswith('currentcluster ='):
                line = f'currentcluster = {repr(new_cluster)}\n'
            print(line, end='')

