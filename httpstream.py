import json
import time
from flask import Flask, Response, request
from agent import gpt_agent_stream
from interpreter import handler


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


def interpreter(msg, env, messages=[]):
    # print(bootName, index, env)
    if msg == 'exit':
        restEnv()
        return 'bye!'
    elif msg == 'ls':
        boots = config.keys()
        res = []
        for b in boots:
            res.append('{} :  {} '.format(b, config[b]['description']))
        return res
    elif msg in config:
        restEnv()
        writer = Writer()
        handler(config[msg]['boot'], writer, input=msg, collect=env.env,
                interruptRead=True)
        env.index = env.env['index']
        env.bootName = msg
        if 'exit' in env.env:
            bootName = env.bootName
            restEnv()
            writer.println('bye ' + bootName + '!')
            return writer.content
        else:
            return writer.content
    elif env.bootName in config:
        writer = Writer()
        handler(config[env.bootName]['boot'], writer, env.index, msg, env.env,
                skipWR=True, interruptRead=True)
        env.index = env.env['index']
        if 'exit' in env.env:
            bootName = env.bootName
            restEnv()
            writer.println('bye ' + bootName + '!')
            return writer.content
        else:
            return writer.content
    else:
        return gpt_agent_stream(msg, messages)


def restEnv():
    env.bootName = ''
    env.env = {}
    env.index = 0


class Writer:

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

    def readline(self):
        return 'hello world'


def inter(req, messages=[]):
    res = interpreter(req, env, messages)
    # print(req, res)
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


def warp(content, stop=False):
    return json.dumps(
      obj={"choices": [{"delta": {"content": content},
                        "finish_reason": "stop" if stop else None}]},
      ensure_ascii=False
    )


def starthttp(config0, port):
    global config
    config = config0
    app.run(port=port)
