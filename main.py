import datetime
import json
import os
import openai
import glob

from openai.error import APIConnectionError, InvalidRequestError

from ClIHandle import ClIHandle
from Log import Log

messages: list[dict] = []
currentFile: str = ""


def generateCompletion(msg):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msg,
        temperature=1,
        n=1,
        stream=False,
        stop=None,
        max_tokens=2048,
        presence_penalty=0,
        frequency_penalty=0,
    )


def parseResult(completions):
    return completions.choices[0]["message"]["content"]


def initOpenAI():
    global messages
    openai.organization = "org-nQ2su19ado3KvvI9HE5vAZHO"
    openai.api_key = os.getenv("OPENAI_API_KEY")
    messages.append({"role": "system", "content": "You are a helpful assistant."})


def chat():
    global messages
    initOpenAI()

    while True:
        Log.point("输入问题")
        content = input()
        if content == "quit":
            save()
            break
        messages.append({"role": "user", "content": content})

        try:
            result = parseResult(generateCompletion(messages))
            messages.append({"role": "assistant", "content": result})
            Log.answer(result)
        except APIConnectionError:
            Log.error("连接超时，请检查网络或稍后再次尝试")
        except InvalidRequestError:
            Log.error("输入文本超过最大限制")


def setFile():
    global currentFile
    path = os.getcwd()
    Log.point("存在的对话文件：")
    for file in glob.glob(os.path.join(path, "*.json")):
        Log.answer(file)

    while True:
        Log.point("请选择一个对话文件")
        fileName = input()
        if fileName == "quit":
            return
        try:
            Log.info("开始读取文件{}".format(fileName))
            with open(fileName, 'r') as f:
                messages.clear()
                currentFile = fileName
                for line in f:
                    item = json.loads(line)
                    messages.append(item)
                Log.info("读取成功,文件信息为：{}".format(messages))
                break
        except FileNotFoundError:
            Log.error("文件不存在")
            continue


def save():
    global messages, currentFile
    fileName = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".json" if currentFile == "" else currentFile
    Log.info("开始保存文件" + fileName)
    with open(fileName, 'w') as f:
        for item in messages:
            json.dump(item, f)
            f.write('\n')
    Log.info("保存成功")


if __name__ == "__main__":
    cli = ClIHandle()
    cli.add("chat", chat)
    cli.add("file", setFile)
    cli.add("save", save)
    while True:
        Log.point("确定你要进行的操作")
        option = input()
        if option == "quit":
            break
        cli.parse(option)
