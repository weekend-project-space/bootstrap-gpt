# bootstrap-gpt

> 引导 GPT 帮助您高效地完成各种任务，gpt-plugin, 可联网，总结网页，突破字数限制，支持 prompt 编排，可自动化, 支持 web api

![bootstrap-gpt](./doc/chat-gpt-simple.gif)

## translate

[中文](./README-CN.md)

## 下载

## 设置 api key

.env

```
api_key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
api_base=https://chatgpt-api.shn.hk/v1/
server_port=9981
```

## 运行

```
cd bootstrap-gpt

pip install openai beautifulsoup4  jsonpath  html2text flask flask-sse

python3 ./main.py
```

## http server

```
> python3 main.py serve


Bootstrap-GPT server v1.0.0

➜ Api: http://localhost:9981/v1/chat/completions
➜ Web: https://weekendproject.space/chat-gpt-online

```

**api**

```
post /v1/chat/completions
{"messages":[{"role":"user","content":"v2-hot"}],"model":"gpt-3.5-turbo"}
```

res

```
{"choices": [{"message": {"role": "assistant", "content": "hello"}]}
```

coordination [chat-gpt-online](https://weekendproject.space/chat-gpt-online.html) Better eating effect

> Note that you need to set an api-key (xxx is enough)

## bootstrap 示例

```
总结网页
------
: summarizelabel
> 请输入网页 $
> $ url
@ spider:{{url}}::select=body art
@ chat:总结一下{{art}} summarize
> 总结: {{m1}} \n还要总结其他网页吗? y/n
> $ yes
^ {{yes}} summarizelabel
```

- . : 标签

- . > 移动/打印

- . < 读取

- . @ 调用自定义过程 spider,chat,len,-,text-len

- . ^ 分支跳转 跳转标签或数字所在行

解释器[interpreter3.py](./interpreter3.py)
