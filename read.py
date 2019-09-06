import json
import os

def read(name):
    with open(name, 'r') as file:
        return [line.rstrip() for line in file]

def get_json(path):
    with open(path, "r") as file:
        d = json.load(file)
        return d

if __name__ == "__main__":
    print(os.path.dirname(os.path.realpath("problems/1/cfg.json")))
    print(get_json("problems/1/cfg.json"))