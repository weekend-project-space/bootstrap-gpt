import os


def listdir(path):
    return os.listdir(path)


def readfile(filename):
    with open(filename, 'r') as file:
        return file.read()
