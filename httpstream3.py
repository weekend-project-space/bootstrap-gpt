import json
import time
from flask import Flask, Response, request
from agent import gpt_agent_stream
from interpreter3 import Bootwarp, IOHolder, handler
from support.fun.function import loadFuncs
import logging

class Env:
    def __init__(self, bootName, env, index) -> None:
        self.bootName = bootName
        self.env = env
        self.index = index


env = Env('', {}, 0)
app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World"


@app.route("/v1/models")
def models():
    return {
            "object": "list",
            "data": [
                {
                    "id": "gpt-3.5-turbo",
                    "object": "model",
                    "created": 1677610602,
                    "owned_by": "openai",
                    "permission": [
                        {
                            "id": "modelperm-lZPGJwrxyPjMHAm856z8yLf8",
                            "object": "model_permission",
                            "allow_create_engine": False,
                            "allow_sampling": True,
                            "allow_logprobs": True,
                            "allow_search_indices": False,
                            "allow_view": True,
                            "allow_fine_tuning": False,
                            "organization": "*",
                            "group": None,
                            "is_blocking": False
                        }
                    ],
                    "root": "gpt-3.5-turbo",
                    "parent": None
                },
            ]
        }


@app.route("/v1/chat/completions", methods=['GET', 'POST'])
def stream():
    msg = request.args.get('msg')
    messages = []
    if not msg:
        req = request.get_json()
        messages = req['messages']
        msg = messages[len(messages)-1]['content']
    return Response(inter(msg, messages), mimetype="text/event-stream")


def interpreter(msg, messages=[]):
    logging.debug(msg)
    bootwarp.io.clear()
    if msg == 'exit':
        restEnv()
        return 'bye!'
    elif msg == 'ls':
        boots = config.keys()
        res = []
        for b in boots:
            res.append('{} :   {} '.format(b, getBootDesc(b)))
        return res
    elif msg in config:
        restEnv()
        bootwarp.boot = getBoot(msg)
        handler(bootwarp, input=msg, interruptRead=True, r=True)
        writer = bootwarp.io
        if not bootwarp.hasNext():
            restEnv()
            writer.println('bye !')
            return writer.content
        else:
            return writer.content
    elif bootwarp.hasBoot():
        handler(bootwarp, input=msg, interruptRead=True, r=True)
        writer = bootwarp.io
        if not bootwarp.hasNext():
            restEnv()
            writer.println('bye !')
            return writer.content
        else:
            return writer.content
    else:
        return gpt_agent_stream(msg, messages)


def restEnv():
    env = loadFuncs(True)
    global bootwarp
    bootwarp = Bootwarp(None, env=env, io=Writer())


class Writer(IOHolder):

    def __init__(self) -> None:
        self.content = []

    def println(self, o):
        if isinstance(o, list):
            for i in o:
                self.content.append(i)
        else:
            self.content.append(o)

    def print(self, o):
        if isinstance(o, list):
            for i in o:
                self.content.append(i)
        else:
            self.content.append(o)

    def clear(self):
        self.content = []


def inter(req, messages=[]):
    res = interpreter(req,  messages)
    if res:
        if isinstance(res, list):
            if len(res) < 3:
                yield warp("  \n".join(res), True)
            else:
                for i in res:
                    time.sleep(0.1)
                    yield warp(' - {} \n'.format(i))
                yield warp(None, True)
        elif isinstance(res, str):
            yield warp(res, True)
        elif isinstance(res, object):
            for event in res:
                yield json.dumps(event, ensure_ascii=False)
        else:
            yield warp(res, True)
    else:
        pass


def getBoot(name):
    lines = config[name].split('\n')
    if len(lines) > 1 and lines[1] == '------':
        return lines[2:]
    else:
        return lines


def getBootDesc(name):
    lines = config[name].split('\n')
    if len(lines) > 1 and lines[1] == '------':
        return lines[0]
    else:
        return name


def warp(content, stop=False):
    return json.dumps(
      obj={"choices": [{"delta": {"content": content},
                        "finish_reason": "stop" if stop else None}]},
      ensure_ascii=False
    )


def startserver(config0, port):
    global config
    config = config0
    env = loadFuncs(True)
    global bootwarp
    bootwarp = Bootwarp(None, env=env, io=Writer())
    print('\n\033[34mBootstrap-GPT server\033[0m v1.0.0 \n')
    print('\033[34m➜\033[0m Api: \033[36m\
http://localhost:{}/v1/chat/completions\033[0m'
          .format(port))
    print('\033[34m➜\033[0m Web: \033[36m\
http://localhost:3000\033[0m')
    print('\n')
    app.run(port=port)
