import cmd
from agent import gpt_agent
from interpreter import handler
from httpserver import startserver
from utils.file import readfile
from utils.parse import parse

env = parse(readfile('.env'))


class Command(cmd.Cmd):
    prompt = '\033[34m>\033[0m '

    def __init__(self, config, completekey='tab', stdin=None, stdout=None):
        super().__init__(completekey=completekey, stdin=stdin, stdout=stdout)
        self.config = config
        self.io = IOHolder(self.stdin, self.stdout, Command.prompt)

    def preloop(self):
        self.io.print('\n\033[34mBootstrap GPT\033[0m\
                       \n\033[35msample > use summarize\033[0m \n \n')

    def do_ls(self, arg):
        boots = self.config.keys()
        for b in boots:
            self.io.print(b)
            self.io.print(' :  ')
            self.io.println(self.config[b]['description'])

    def do_use(self, arg):
        if arg in self.config:
            boot = self.config[arg]['boot']
            handler(boot, self.io)
            self.io.println('bye '+arg+'!')
        else:
            self.io.println('\033[31mnot found bootstarap: '+arg+'!\033[0m ')

    def do_serve(self, arg):
        startserver(self.config, int(env['server_port']))

    def do_chat(self, arg):
        self.io.println('chat: {}'.format(gpt_agent(arg)))

    def do_exit(self, arg):
        self.io.println('Exiting...')
        return True


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
