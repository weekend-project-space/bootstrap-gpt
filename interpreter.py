from agent import agent
from utils.templateEngine import render


# w:write p:prompt b:branch Array next, Obj switch
def handler(boot, io=None, index=0, input='', collect={}, skipWR=False,
            interruptRead=False):
    inst = boot[index]
    write = inst['w'] if 'w' in inst else None
    read = inst['r'] if 'r' in inst else None
    prompt = inst['p'] if 'p' in inst else None
    branch = inst['b'] if 'b' in inst else None
    msg = input
    size = len(boot)

    collect['index'] = index

    if not skipWR:
        if write:
            content = render(write, collect)
            collect['w'+str(index)] = content
            io.println(content)
        else:
            pass

        if read:
            if interruptRead:
                return msg
            else:
                io.print('\033[34m>\033[0m ')
                msg = io.readline()
                collect[read] = msg
        else:
            collect['r'+str(index)] = input
    else:
        if read:
            collect[read] = input
        else:    
            collect['r'+str(index)] = input

    if prompt:
        content = render(prompt, collect)
        collect['p'+str(index)] = content
        msg = agent(content, collect, prompt)
        collect['m'+str(index)] = msg
    else:
        pass

    if branch:
        if isinstance(branch, list):
            for i in branch:
                msg = handler(boot, io, i, msg, collect, False, interruptRead)
        elif isinstance(branch, object):
            key = str(msg)
            if key in branch:
                index0 = branch[key]
                if int(index0) < 0:
                    collect['exit'] = True
                    return key
                else:
                    msg = handler(boot, io, index0, msg, collect, False,
                                  interruptRead)
            elif index+1 < size:
                msg = handler(boot, io, index+1, msg, collect, False,
                              interruptRead)
            else:
                pass
        else:
            pass
    elif index+1 < size:
        msg = handler(boot, io, index+1, msg, collect, False, interruptRead)
    else:
        collect['exit'] = True
    return msg
