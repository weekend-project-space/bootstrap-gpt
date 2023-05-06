import sys
from support.fun.function import loadFuncs
from utils.file import readfile


class Instr:

    def __init__(self, key, args, target) -> None:
        self.key = key
        self.args = args
        self.target = target

    def __str__(self) -> str:
        return (self.key, self.args, self.target).__str__()


class Bootwarp:

    def __init__(self, boot, index=0, env={}, io=None) -> None:
        self.boot = boot
        self.index = index
        self.env = env
        self.io = io

    def read(self) -> Instr:
        instr_str = self.boot[self.index].strip()
        left_index = instr_str.find(" ")
        right_index = instr_str.rfind(" ")
        key = instr_str[0:left_index]
        args = instr_str[left_index+1:]
        target = None
        if right_index != left_index:
            args = instr_str[left_index+1: right_index]
            target = instr_str[right_index+1:]
        return Instr(key, args, target)

    def setIndex(self, index=0):
        self.index = index

    def hasNext(self) -> bool:
        return len(self.boot)-1 > self.index and self.index > -1

    def next(self):
        self.index += 1


class IOHolder:

    def __init__(self,  stdin=sys.stdin, stdout=sys.stdout, prompt='>'):
        self.stdin = stdin
        self.stdout = stdout
        self.prompt = prompt

    def println(self, o):
        if isinstance(o, list):
            for i in o:
                self.stdout.write(i)
                self.stdout.write('\n')
        else:
            self.stdout.write(o)
        self.stdout.write('\n')
        self.stdout.flush()

    def print(self, o):
        self.stdout.write(o)
        self.stdout.flush()

    def readline(self):
        line = self.stdin.readline()
        if not len(line):
            line = 'EOF'
        else:
            line = line.rstrip('\r\n')
        return line


def inter(bootwarp, instr):
    func = bootwarp.env[instr.key]
    if func:
        func(bootwarp, instr)
    else:
        bootwarp.io.println('error: undefind '+instr.key)


def handler(bootwarp, interruptRead=False):
    instr = bootwarp.read()
    # print(instr)
    inter(bootwarp, instr)
    if bootwarp.hasNext():
        bootwarp.next()
        handler(bootwarp)
    pass


if __name__ == '__main__':
    env = loadFuncs()
    boot = readfile('./demo.bs').split('\n')
    handler(Bootwarp(boot, env=env, io=IOHolder()))
