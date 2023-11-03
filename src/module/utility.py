import json


def json_file_load(filename: str) -> dict:
    f = open(filename, 'r')
    return json.load(f)


def json_file_save(filename: str, data: dict):
    f = open(filename, 'w')
    json.dump(data, f, indent=4)


def json_file_read(filename: str, key: str):
    data = json_file_load(filename)
    return data[key]


def json_file_write(filename: str, key: str, value):
    data = json_file_load(filename)
    data[key] = value
    json_file_save(filename, data)
