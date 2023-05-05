# bootstrap-gpt

> Guide GPT to help you efficiently complete various tasks, write GPT prompts programs, and automate GPT prompts, support web api

![bootstrap-gpt](./doc/gpt-online-demo.gif)

![bootstrap-gpt](./doc/screen.png)

## translate

[中文](./README-CN.md)

## download

## set api key

.env

```
api_key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
api_base=https://chatgpt-api.shn.hk/v1/
server_port=9981
```

## run

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

## bootstrap simple

```
{
    "author": "ruidong",
    "date": "2023-04-17",
    "version": "0.1",
    "description": "code boot",
    "boot": [{
            "w": "Hello, this is a code template. Please select template 1. simple 2. demo",
            "r":"r0",
            "b": {
                "1": 1,
                "2": 2
            }
        },
        {
            "w": "Please enter the language type"
            "r":"r1",
        },
        {
            "w": "Please enter the requirement",
            "r":"r2",
            "p": "chat:Write a {{r2}} program for {{r1}}"
        }
    ]
}
```

- w: write supports template variables

- r: read

- b: Branch branch supports object field eq jump and Array sequential execution or no further execution

- p: prompt supports template variable micro instructions for guiding chatgt [chat:] to search for plain text or crawler [spider:] output, which can expand more micro instruction prompt guidance

r2 r1 is a variable with a name of type and an index of r: reader w: writer p: prompts m: msg

Generate Rule Reference [interpreter.py](./interpreter.py)
