from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from agent import gpt_agent
from interpreter import handler
from utils.parse import parse


PORT = 8080

config = {}


class Env:
    def __init__(self, bootName, env, index) -> None:
        self.bootName = bootName
        self.env = env
        self.index = index


env = Env('', {}, 0)


class RequestHandler(BaseHTTPRequestHandler):

    def handler(self):
        print("data:", self.rfile.readline().decode())
        self.wfile.write(self.rfile.readline())

    def do_GET(self):
        if self.path == '/favicon.ico':
            return
        self.query = self.path.split('?')[1]
        params = parse(self.query, '&')
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        data = {'data': interpreter(params['msg'], env)}
        self.wfile.write(json.dumps(data, ensure_ascii=False)
                         .encode('utf-8'))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        req_datas = self.rfile.read(int(self.headers['content-length']))
        data = {'data': interpreter(req_datas['msg'], env)}
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
            return 'bye ' + bootName + '!'
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
            return 'bye ' + bootName + '!'
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





def startserver(config0):
    global config
    config = config0
    server = HTTPServer(('localhost', 8080), RequestHandler)
    print('HTTP Server running on port 8080')
    server.serve_forever()
