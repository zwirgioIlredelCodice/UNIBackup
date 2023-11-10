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


class colors:
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'


class prettyPrint:
    def ok(text: str):
        print(colors.fg.green, text, colors.reset)

    def warn(text: str):
        print(colors.fg.orange, text, colors.reset)

    def err(text: str):
        print(colors.fg.red, text, colors.reset)
