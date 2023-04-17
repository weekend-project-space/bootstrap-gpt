import openai
import requests
from bs4 import BeautifulSoup
from utils.file import readfile
from utils.env import parse


# 设置 OpenAI API 密钥
openai.api_key = parse(readfile('.env'))['api_key']


def spider(query):
    url = query
    select = 'body'
    if query.find(':select=') > 0:
        arr = query.split(':select=')
        url = arr[0]
        select = arr[1]
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
              (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup.select_one(select).get_text()


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


def agent(content):
    index = content.find(':')
    agentName = content[:index]
    promt = content[index+1:]
    # print(str(index)+agentName+'---' + promt)
    if agentName == 'chat':
        return gpt_agent(promt)
    else:
        if agentName == 'spider':
            return spider(promt)
        else:
            return promt
