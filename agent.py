import openai
import requests
from bs4 import BeautifulSoup
from utils.file import readfile
from utils.env import parse
from utils.json import to_obj
from jsonpath import jsonpath

env = parse(readfile('.env'))
# 设置 OpenAI API 密钥
openai.api_key = env['api_key']
openai.api_base = env['api_base']


def spider(query):
    url = query
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
              (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    if query.find(':select=') > 0:
        arr = query.split(':select=')
        url = arr[0]
        select = arr[1]
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        return soup.select_one(select).get_text()
    elif query.find(':jsonpath=') > 0:
        arr = query.split(':jsonpath=')
        url = arr[0]
        path = arr[1]
        res = requests.get(url, headers=headers)
        return jsonpath(to_obj(res.text), path)
    else:
        v = requests.get(url, headers=headers)
        return v.text


def gpt_agent(content):
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
    v = env[kv[1].trim()]
    env[kv[0].trim()] = v
    return v


def agent(content, env, prompt):
    index = content.find(':')
    agentName = content[:index]
    promp = content[index+1:]
    # print(str(index)+agentName+'---' + promt)
    if agentName == 'chat':
        return gpt_agent(promp)
    elif agentName == 'spider':
        return spider(promp)
    elif agentName == '-':
        return decrease(env, promp)
    elif agentName == '+':
        return increase(env, promp)
    elif agentName == 'set!':
        return set(env, promp)
    elif agentName == 'len':
        return len0(env, promp)
    else:
        return promp
