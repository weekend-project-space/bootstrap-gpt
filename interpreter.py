from agent import agent
from utils.templateEngine import render


# w:write p:prompt b:branch Array next, Obj switch
def handler(boot, io, index=0, input='', collect={}):
    inst = boot[index]
    out = inst['w'] if 'w' in inst else None
    prompt = inst['p'] if 'p' in inst else None
    branch = inst['b'] if 'b' in inst else None
    msg = input
    size = len(boot)

    if out:
        content = render(out, collect)
        collect['w'+str(index)] = content
        io.print(content+'\n> ')
        msg = io.readline()
        if not len(msg):
            msg = 'EOF'
        else:
            msg = msg.rstrip('\r\n')
            collect['r'+str(index)] = msg
    else:
        collect['r'+str(index)] = msg

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
                msg = handler(boot, io, i, msg, collect)
        elif isinstance(branch, object):
            key = str(msg)
            if key in branch:
                index0 = branch[key]
                if int(index0) < 0:
                    return key
                else:
                    msg = handler(boot, io, index0, msg, collect)
            elif index+1 < size:
                msg = handler(boot, io, index+1, msg, collect)
            else:
                pass
        else:
            pass
    elif index+1 < size:
        msg = handler(boot, io, index+1, msg, collect)
    else:
        pass

    return msg
