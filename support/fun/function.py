from utils.templateEngine import render
from agent import agent


def println(bootwarp, instr, interruptRead=False):
    r = render(instr.args, bootwarp.env)
    if r.find('\\n') > -1:
        r = r.replace('\\n', '\n')
    if r == '$':
        if not interruptRead:
            bootwarp.io.print('\033[34m>\033[0m ')
        r = bootwarp.io.readline()
    else:
        pass
    if instr.target and instr.target != '$':
        bootwarp.env[instr.target] = r
    else:
        bootwarp.io.println(r)


def read(bootwarp, instr, interruptRead=False):
    if not interruptRead:
        bootwarp.io.print('\033[34m>\033[0m ')
    msg = bootwarp.io.readline()
    bootwarp.env[instr.args] = msg


def jump(bootwarp, instr):
    flag = render(instr.args, bootwarp.env)
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


def loadFuncs(interruptRead=False) -> dict:
    env = {}
    env['>'] = lambda bootwarp, instr: println(bootwarp, instr, interruptRead)
    env['<'] = lambda bootwarp, instr: read(bootwarp, instr, interruptRead)
    env['^'] = jump
    env[':'] = label
    env['@'] = call
    return env
