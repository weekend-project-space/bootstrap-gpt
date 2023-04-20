from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from agent import gpt_agent
from interpreter import handler
from utils.parse import parse


PORT = 8080

config = {}
collect = {}

class RequestHandler(BaseHTTPRequestHandler):

    def handler(self):
        print("data:", self.rfile.readline().decode())
        self.wfile.write(self.rfile.readline())

    def do_GET(self):
        self.query = self.path.split('?', 1)[1]
        params = parse(self.query, '&')
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        response = {'data': handler0(params['msg'],
                    params['bootname'] if 'bootname' in params else None,
                    int(params['index']) if 'index' in params else 0, collect)}
        self.wfile.write(json.dumps(response, ensure_ascii=False)
                         .encode('utf-8'))

    def do_POST(self):
        print(self.headers)
        print(self.command)
        req_datas = self.rfile.read(int(self.headers['content-length']))
        print(req_datas.decode())
        data = {
            'result_code': '2',
            'result_desc': 'Success',
            'timestamp': '',
            'data': {'message_id': '25d55ad283aa400af464c76d713c07ad'}
        }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))


def handler0(msg, bootName, index, env):
    # print(bootName, index, env)
    if msg == 'ls':
        boots = config.keys()
        str = ''
        for b in boots:
            str += '{} :  {} \n '.format(b, config[b]['description'])
        return str
    elif msg in config:
        env['w'] = []
        handler(config[msg]['boot'], input=msg, collect=env,
                interrupt=True)
        print('---', env['index'])
        return env['w']
    elif bootName in config:
        env['w'] = []
        handler(config[bootName]['boot'], None, index, msg, env,
                skipout=True)
        print(env['index'])
        return env['w']
    else:
        return gpt_agent(msg)


def startserver(config0):
    global config
    config = config0
    server = HTTPServer(('localhost', 8080), RequestHandler)
    print('HTTP Server running on port 8080')
    server.serve_forever()
