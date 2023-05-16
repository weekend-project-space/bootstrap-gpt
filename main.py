import sys
from command import Command
from utils.file import listdir, readfile
from httpstream3 import startserver
from env import env


def loadConfig():
    path = "bootstrap"
    dir = listdir(path)
    config = {}
    for filename in dir:
        file = path+'/'+filename
        config[filename.replace('.bs', '')] = readfile(file)
    return config


def main(args):
    severPort = int(env['server_port'])
    if len(args) > 1 and args[1] == 'serve':
        startserver(loadConfig(), severPort)
    else:
        Command(loadConfig(), severPort).cmdloop()


if __name__ == '__main__':
    main(sys.argv)
