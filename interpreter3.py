import sys
# import logging


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
        self.index = 0
        self.env = env
        self.io = io
        self.initLable()
        self.index = index

    def initLable(self):
        if self.boot:
            for i in range(len(self.boot)):
                instr = Bootwarp.getInstr0(self.boot, i)
                if instr.key == ':':
                    self.env[instr.args] = i

    def getInstr(self) -> Instr:
        return Bootwarp.getInstr0(self.boot, self.index)

    def getInstr0(boot, index) -> Instr:
        instr_str = boot[index].strip()
        left_index = instr_str.find(" ")
        right_index = instr_str.rfind(" ")
        key = instr_str[0:left_index]
        args = instr_str[left_index+1:]
        target = None
        if right_index != left_index:
            args = instr_str[left_index+1: right_index]
            target = instr_str[right_index+1:]
        return Instr(key, args, target)

    def setBoot(self, boot):
        self.boot = boot
        self.index = 0
        self.initLable()
        self.index = 0

    def setIndex(self, index=0):
        self.index = index

    def hasNext(self) -> bool:
        return self.boot and len(self.boot)-1 > self.index and self.index > -1

    def next(self):
        self.index += 1

    def isReadInstr(self):
        instr = self.getInstr()
        if instr.key == '<':
            return True
        elif instr.key == '>' and instr.args == '$':
            return True
        else:
            return False

    def hasBoot(self):
        return True if self.boot else False


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
        if self.line:
            line = self.line
            self.line = None
            return line
        else:
            line = self.stdin.readline()
            if not len(line):
                line = 'EOF'
            else:
                line = line.rstrip('\r\n')
            return line

    def setLine(self, str):
        self.line = str


def inter0(bootwarp, instr):
    func = bootwarp.env[instr.key]
    if func:
        func(bootwarp, instr)
    else:
        bootwarp.io.println('error: undefind '+instr.key)


def handler(bootwarp, input=None, interruptRead=False, r=False):
    # logging.info(input, bootwarp.index)
    if interruptRead and bootwarp.isReadInstr() and not r:
        return True
    else:
        if bootwarp.isReadInstr() and input:
            bootwarp.io.setLine(input)
        else:
            pass
        instr = bootwarp.getInstr()
        inter0(bootwarp, instr)
        if bootwarp.hasNext():
            bootwarp.next()
            handler(bootwarp, input, interruptRead)
        pass


# if __name__ == '__main__':
#     env = loadFuncs()
#     boot = readfile('./demo.bs').split('\n')
#     handler(Bootwarp(boot, env=env, io=IOHolder()))
