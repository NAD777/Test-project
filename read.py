import json
import os


def read(name):
    with open(name, 'r') as file:
        return [line.rstrip() for line in file]


def get_json(path):
    with open(path, "r") as file:
        d = json.load(file)
        return d


def get_tests(col, dir):
    arr = sorted(filter(lambda x: not x.endswith(".a"), os.listdir(f"problems/{dir}/tests")),
                 key=lambda x: int(x))
    ret = []
    for i in range(min(col, len(arr))):
        ret.append((read(f"problems/{dir}/tests/{arr[i]}"),
                    read(f"problems/{dir}/tests/{arr[i]}.a")))
    return ret


def remove_folder(path):
    for el in os.walk(path, topdown=False):
        print(el)
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(os.path.join(path))


if __name__ == "__main__":
    get_tests(2, '6')
