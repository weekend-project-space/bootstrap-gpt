from utils.templateEngine import render
from agent import agent


def println(bootwarp, instr):
    r = render(instr.args, bootwarp.env)
    if r == '$':
        bootwarp.io.print('\033[34m>\033[0m ')
        r = bootwarp.io.readline()
    else:
        pass
    if instr.target and instr.target != '$':
        bootwarp.env[instr.target] = r
    else:
        bootwarp.io.println(r)


def read(bootwarp, instr):
    bootwarp.io.print('\033[34m>\033[0m ')
    msg = bootwarp.io.readline()
    bootwarp.env[instr.args] = msg


def jump(bootwarp, instr):
    flag = render(instr.args, bootwarp.env)
    print(flag)
    if flag != 0 and flag != '0' and flag:
        label = render(instr.target, bootwarp.env)
        if isinstance(label, str):
            label = bootwarp.env[label]
        else:
            pass
        index = int(label)
        bootwarp.setIndex(index)
    else:
        pass


def label(bootwarp, instr):
    bootwarp.env[instr.args] = bootwarp.index


def call(bootwarp, instr):
    r = render(instr.args, bootwarp.env)
    bootwarp.env[instr.target] = agent(r, bootwarp.env, instr.args)


def loadFuncs() -> dict:
    env = {}
    env['>'] = println
    env['<'] = read
    env['^'] = jump
    env[':'] = label
    env['@'] = call
    return env
