import openai
import requests
from bs4 import BeautifulSoup
from utils.json import to_obj
from jsonpath import jsonpath
from env import env
from utils.parse import parse
import html2text as ht

# print(env)
# 设置 OpenAI API 密钥
openai.api_key = env['api_key']
openai.api_base = env['api_base']


def spider(query):
    url = query
    params = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
              (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    if query.find('::'):
        arr = query.split('::')
        url = arr[0]
        params = parse(arr[1], '&')
    else:
        pass

    res = requests.get(url, headers=headers)
    if 'select' in params:
        soup = BeautifulSoup(res.text, "html.parser")
        return soup.select_one(params['select']).get_text()
    elif 'jsonpath' in params:
        return jsonpath(to_obj(res.text), params['jsonpath'])
    elif 'tojson' in params:
        return to_obj(res.text)
    else:
        return res.text


def gpt_agent(content):
    # print(content)
    # 创建 OpenAI GPT 对象
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": content},
        ]
    )

    result = ''
    for choice in response.choices:
        result += choice.message.content
    return result


def gpt_agent_stream(content, messages):
    if len(messages) < 2:
        messages = [
            {"role": "user", "content": content},
        ]
    # print(content)
    # 创建 OpenAI GPT 对象
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True
    )
    return response


def decrease(env, key):
    v = int(env[key])-1
    env[key] = v
    return v


def increase(env, key):
    v = int(env[key])+1
    env[key] = v
    return v


def len0(env, key):
    return len(env[key])


def set(env, exp):
    kv = exp.split('=')
    k = kv[0].trim()
    v = kv[1].trim()
    v = env[v] if v in env else v
    if k in env:
        env[k] = v
        return v
    else:
        return None


def define(env, exp):
    kv = exp.split('=')
    k = kv[0].trim()
    v = kv[1].trim()
    v = env[v] if v in env else v
    if k in env:
        return None
    else:
        env[k] = v
        return v


def html2md(data):
    text_maker = ht.HTML2Text()
    text_maker.bypass_tables = False
    md = text_maker.handle(data)
    return md


def agent(content, env, prompt):
    index = content.find(':')
    agentName = content[:index]
    promp = content[index+1:]
    # print(str(index)+agentName+'---' + promt)
    if agentName == 'chat':
        return gpt_agent(promp)
    elif agentName == 'spider':
        return spider(promp)
    elif agentName == 'html2md':
        return html2md(promp)
    elif agentName == '-':
        return decrease(env, promp)
    elif agentName == '+':
        return increase(env, promp)
    elif agentName == 'set!':
        return set(env, promp)
    elif agentName == 'define':
        return define(env, promp)
    elif agentName == 'len':
        return len0(env, promp)
    else:
        return promp
