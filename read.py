def read(name):
    with open(name, 'r') as file:
        return [line.rstrip() for line in file]