import json
import logging
import re
import openai
import requests
from bs4 import BeautifulSoup
from utils.json import to_obj
from jsonpath import jsonpath
from env import env
from utils.parse import parseone
import html2text as ht

reg = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F]'\
    + '[0-9a-fA-F]))+'
# print(env)
# 设置 OpenAI API 密钥
openai.api_key = env['api_key']
openai.api_base = env['api_base']


def spider(query):
    url = query
    params = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
              (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        'cookie': 'session-id=138-0644453-6275916; i18n-prefs=USD; sp-cdn="L5Z9:HK"; ubid-main=130-6986158-5946839; lc-main=en_US; session-token="li6hr/FTfjgE1a8nr6b1Z+kN4JWGJto4r+bsr6Adi5lO/9KbFyuZRJlpxS7saJctez9NOAxGElxb/IgS9D2TMhRWWNo4MUYGZov65y0sMSqLI4xKj2F8FGjHLlpYSna1rGBUfOz37tOhbF9j6LmxAHbe4AyOdblweKsPP6XHbDZuPVW3F/OK6NPmUIeq5dl1Lo5PmhHQYW0zYJaflPhpqkyUni/5HQTm543C+B+7LG0="; session-id-time=2082787201l; csm-hit=tb:s-SFFN9CRT3AD16RZ86ZZD|1683878824743&t:1683878824918&adb:adblk_yes'}

    if query.find('::') > 0:
        arr = query.split('::')
        url = arr[0]
        params = parseone(arr[1], '=')
    else:
        pass
    res = requests.get(url, headers=headers)
    # print(query, params, url)
    if 'select' in params:
        soup = BeautifulSoup(res.text, "html.parser")
        t = soup.select(params['select'])
        str = ''
        for item in t:
            str += item.get_text()
        return str
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
    if len(messages) > 1:
        messages[len(messages)-1]['content'] = content
    # print(content)
    # 创建 OpenAI GPT 对象
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True
    )
    return response


def gpt_agent_http_stream(content, messages):
    str = _link2text(content)
    # print(str)
    return gpt_agent_stream(str, messages)


def _link2text(content):
    links = re.findall(reg, content)
    for link in links:
        text = spider('{}::select=body'.format(link)).strip()
        content = content.replace(link, '{}'.format(text))
    return content


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


def textlen0(data):
    if data == 'None':
        return 0
    else:
        return len(data)


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
    promp = content[index+1:].strip()
    # print(promp)
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
    elif agentName == 'text-len':
        return textlen0(promp)
    else:
        return promp
