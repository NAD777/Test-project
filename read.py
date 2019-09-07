import json


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


if __name__ == "__main__":
    print(repr(string_to_dict("1 2~3|3 4~7")))
