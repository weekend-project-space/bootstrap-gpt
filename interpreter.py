from agent import agent
from utils.templateEngine import render


# o:output t:template b:branch Array next, Obj switch
def handler(boot, io, index=0, input='', collect={}):
    inst = boot[index]
    out = inst['o'] if 'o' in inst else None
    template = inst['t'] if 't' in inst else None
    branch = inst['b'] if 'b' in inst else None
    msg = input
    if out:
        content = render(out, collect)
        io.print(content+'\n> ')
        msg = io.readline()
        if not len(msg):
            msg = 'EOF'
        else:
            msg = msg.rstrip('\r\n')
            collect['r'+str(index)] = msg
    else:
        collect['r'+str(index)] = msg

    if template:
        content = render(template, collect)
        collect['p'+str(index)] = content
        msg = agent(content)
        collect['m'+str(index)] = msg
    else:
        pass
    if branch:
        if isinstance(branch, list):
            for i in branch:
                msg = handler(boot, io, i, msg, collect)
        else:
            if isinstance(branch, object):
                index0 = branch[msg]
                msg = handler(boot, io, index0, msg, collect)
            else:
                pass
    return msg
