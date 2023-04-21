from command import Command
from utils.file import listdir
from utils.json import read_file_to_json


def loadConfig():
    path = "bootstrap"
    dir = listdir(path)
    config = {}
    for filename in dir:
        file = path+'/'+filename
        config[filename.replace('.json', '')] = read_file_to_json(file)
    return config


if __name__ == '__main__':
    Command(loadConfig()).cmdloop()
