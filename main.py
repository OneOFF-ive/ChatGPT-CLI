import datetime
import json
import os
import openai
import glob
from ClIHandle import ClIHandle

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
        max_tokens=3012,
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
        content = input()
        if content == "quit":
            save()
            break
        messages.append({"role": "user", "content": content})

        result = parseResult(generateCompletion(messages))
        messages.append({"role": "assistant", "content": result})
        print(result)


def setFile():
    global currentFile
    path = os.getcwd()
    for file in glob.glob(os.path.join(path, "*.json")):
        print(file)

    while True:
        fileName = input("选择文件：")
        if fileName == "quit":
            return
        try:
            with open(fileName, 'r') as f:
                messages.clear()
                currentFile = fileName
                for line in f:
                    item = json.loads(line)
                    messages.append(item)
                print(messages)
                break
        except FileNotFoundError:
            print("文件不存在")
            continue


def save():
    global messages, currentFile
    fileName = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") if currentFile == "" else currentFile
    with open(fileName + ".json", 'w') as f:
        for item in messages:
            json.dump(item, f)
            f.write('\n')


if __name__ == "__main__":
    cli = ClIHandle()
    cli.add("chat", chat)
    cli.add("file", setFile)
    cli.add("save", save)
    while True:
        option = input("选项：")
        if option == "quit":
            break
        cli.parse(option)
