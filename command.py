import cmd
from agent import gpt_agent
from interpreter3 import Bootwarp, handler
from httpstream3 import startserver
from support.fun.function import loadFuncs


class Command(cmd.Cmd):
    prompt = '\033[34m>\033[0m '

    def __init__(self, config, severPort, completekey='tab', stdin=None,
                 stdout=None):
        super().__init__(completekey=completekey, stdin=stdin, stdout=stdout)
        self.config = config
        self.severPort = severPort
        self.io = IOHolder(self.stdin, self.stdout, Command.prompt)

    def preloop(self):
        self.io.print('\n\033[34mBootstrap GPT\033[0m\
                       \n\033[35msample > use summarize\033[0m \n \n')

    def do_ls(self, arg):
        boots = self.config.keys()
        print(self.config)
        for b in boots:
            self.io.println('{} :  {} '
                            .format(b, getBootDesc(self.config, b)))

    def do_use(self, arg):
        if arg in self.config:
            boot = getBoot(self.config, arg)
            env = loadFuncs()
            bootwarp = Bootwarp(boot, env=env, io=self.io)
            handler(bootwarp)
            self.io.println('bye '+arg+'!')
        else:
            self.io.println('\033[31mnot found bootstarap: '+arg+'!\033[0m ')

    def do_serve(self, arg):
        startserver(self.config, self.severPort)

    def do_chat(self, arg):
        self.io.println('chat: {}'.format(gpt_agent(arg)))

    def do_exit(self, arg):
        self.io.println('Exiting...')
        return True


def getBoot(config, name):
    lines = config[name].split('\n')
    if len(lines) > 1 and lines[1] == '------':
        return lines[2:]
    else:
        return lines


def getBootDesc(config, name):
    lines = config[name].split('\n')
    if len(lines) > 1 and lines[1] == '------':
        return lines[0]
    else:
        return name


class IOHolder:

    def __init__(self,  stdin=None, stdout=None, prompt='>'):
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
