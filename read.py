import json
import os


def read(name):
    with open(name, 'r') as file:
        return [line.rstrip() for line in file]


def get_json(path):
    with open(path, "r") as file:
        d = json.load(file)
        return d


def string_to_dict(string):  # "1 2~3|3 4~7" -> dict("1 2": "3", "3 4": "7")
    d = dict()
    for text_with_ans in string.split('|'):
        test, ans = text_with_ans.split('~')
        d[test] = ans
    return d


def get_tests(col, dir):
    arr = sorted(filter(lambda x: not x.endswith(".a"), os.listdir(f"problems/{dir}/tests")), key=lambda x: int(x))
    ret = []
    for i in range(col):
        ret.append((read(f"problems/{dir}/tests/{arr[i]}"), read(f"problems/{dir}/tests/{arr[i]}.a")))
    return ret


if __name__ == "__main__":
    get_tests(2, '6')
    # print(repr(string_to_dict("1 2~3|3 4~7")))
