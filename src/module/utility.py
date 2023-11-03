import json


def json_file_load(filename: str) -> dict:
    f = open(filename, 'r')
    data = f.read()

    return json.load(data)


def json_file_save(filename: str, data: dict):
    jdata = json.dumps(data, indent=4)

    f = open(filename, 'w')
    f.write(jdata)


def json_file_read(filename: str, key: str):
    data = json_file_load(filename)
    return data[key]


def json_file_write(filename: str, key: str, value):
    data = json_file_load(filename)
    data[key] = value
    json_file_save(filename, data)
