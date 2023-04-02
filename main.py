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
    Log.point("Start Chatting")
    while True:
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
    Log.point("Existing Files：")
    for file in glob.glob(os.path.join(path, "*.json")):
        Log.answer(file)

    while True:
        Log.point("Select A File")
        fileName = input()
        if fileName == "quit":
            return
        try:
            Log.info("Loading File {}".format(fileName))
            with open(fileName, 'r') as f:
                messages.clear()
                currentFile = fileName
                for line in f:
                    item = json.loads(line)
                    messages.append(item)
                Log.info("Loaded File {}, Messages Is {}".format(fileName, messages))
                break
        except FileNotFoundError:
            Log.error("File Does Not Exist")
            continue


def save():
    global messages, currentFile
    fileName = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".json" if currentFile == "" else currentFile
    Log.info("Saving File {}".format(fileName))
    with open(fileName, 'w') as f:
        for item in messages:
            json.dump(item, f)
            f.write('\n')
    Log.info("Saved File {}".format(fileName))


if __name__ == "__main__":
    Log.info("Project Launch")
    cli = ClIHandle()
    cli.add("chat", chat)
    cli.add("file", setFile)
    cli.add("save", save)
    while True:
        Log.point("Action")
        option = input()
        if option == "quit":
            break
        cli.parse(option)
