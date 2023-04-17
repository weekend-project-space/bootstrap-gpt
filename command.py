import cmd
from agent import gpt_agent
from interpreter import handler


class Command(cmd.Cmd):
    prompt = '> '

    def __init__(self, config, completekey='tab', stdin=None, stdout=None):
        super().__init__(completekey=completekey, stdin=stdin, stdout=stdout)
        self.config = config
        self.io = IOHolder(self.stdin, self.stdout, Command.prompt)

    def preloop(self):
        self.io.print('Welcome to WeBootstrap GPT\nsample > use ppt \n')

    def do_ls(self, arg):
        boots = self.config.keys()
        for b in boots:
            self.io.println(b)

    def do_use(self, arg):
        boot = self.config[arg]['boot']
        self.io.println(handler(boot, self.io))
        self.io.println('bye '+arg+'!')

    def do_chat(self, arg):
        self.io.println('chat, {}'.format(gpt_agent(arg)))

    def do_exit(self, arg):
        self.io.println('Exiting...')
        return True


class IOHolder:

    def __init__(self,  stdin=None, stdout=None, prompt='>'):
        self.stdin = stdin
        self.stdout = stdout
        self.prompt = prompt

    def println(self, o):
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
