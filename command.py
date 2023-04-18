import cmd
from agent import gpt_agent
from interpreter import handler


class Command(cmd.Cmd):
    prompt = '\033[34m>\033[0m '

    def __init__(self, config, completekey='tab', stdin=None, stdout=None):
        super().__init__(completekey=completekey, stdin=stdin, stdout=stdout)
        self.config = config
        self.io = IOHolder(self.stdin, self.stdout, Command.prompt)

    def preloop(self):
        self.io.print('\033[34mWelcome to WeBootstrap GPT\033[0m\
                       \n\033[35msample > use friend\033[0m \n')

    def do_ls(self, arg):
        boots = self.config.keys()
        for b in boots:
            self.io.println(b)

    def do_use(self, arg):
        if arg in self.config:
            boot = self.config[arg]['boot']
            self.io.println(handler(boot, self.io))
            self.io.println('bye '+arg+'!')
        else:
            self.io.println('\033[31mnot found bootstarap: '+arg+'!\033[0m ')

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
