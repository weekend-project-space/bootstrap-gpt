import json
from utils.file import readfile


def read_file_to_json(filename):
    return json.loads(readfile(filename))
