from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
from agent import gpt_agent
from interpreter import handler
from utils.parse import parse

config = {}


class Env:
    def __init__(self, bootName, env, index) -> None:
        self.bootName = bootName
        self.env = env
        self.index = index


env = Env('', {}, 0)


class RequestHandler(SimpleHTTPRequestHandler):

    def _cors_header(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Headers', '*')

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors_header()
        self.end_headers()

    def do_GET(self):
        if self.path == '/favicon.ico':
            return
        self.query = self.path.split('?')[1]
        params = parse(self.query, '&')
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        res = interpreter(params['msg'], env)
        data = {'data': res}
        self.wfile.write(json.dumps(data, ensure_ascii=False)
                         .encode('utf-8'))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self._cors_header()
        self.end_headers()
        req_datas = self.rfile.read(int(self.headers['content-length']))

        if self.path.find('/v1/chat/completions') == 0:
            req = json.loads(req_datas)['messages'][0]['content']
            res = interpreter(req.replace('\n', ''), env)
            # print(len(res))
            if isinstance(res, list):
                if len(res) < 3:
                    res = "  \n".join(res)
                else:
                    res = "  \n - ".join(res)
                    res = ' - '+res
            data = {"choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": res
                    }
                }]}
        else:
            res = interpreter(req_datas['msg'], env)
            data = {'data': res}
        self.wfile.write(json.dumps(data).encode('utf-8'))


def interpreter(msg, env):
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
        return gpt_agent(msg)


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


def startserver(config0, port):
    global config
    config = config0
    server = HTTPServer(('0.0.0.0', port), RequestHandler)
    print('\n\033[34mBootStrap-GPT server\033[0m v1.0.0 \n')
    print('\033[34m➜\033[0m Api: \033[36m\
http://localhost:{}/v1/chat/completions\033[0m'
          .format(port))
    print('\033[34m➜\033[0m Web: \033[36m\
https://weekendproject.space/chat-gpt-online\033[0m')
    print('\n')
    server.serve_forever()
