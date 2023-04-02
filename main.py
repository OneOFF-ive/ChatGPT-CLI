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

model: str = "gpt-3.5-turbo"
temperature: int = 1
n: int = 1
stream: bool = True
stop: bytes = None
max_tokens: int = 2048
presence_penalty: int = 0
frequency_penalty: int = 0


def generateCompletion(msg):
    global model, temperature, n, stream, stop, max_tokens, presence_penalty, frequency_penalty
    response = openai.ChatCompletion.create(
        model=model,
        messages=msg,
        temperature=temperature,
        n=n,
        stream=stream,
        stop=stop,
        max_tokens=max_tokens,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty,
    )
    return response


def parseResult(completions):
    result = completions.choices[0]["message"]["content"]
    messages.append({"role": "assistant", "content": result})
    Log.answer(result)
    Log.info("Finish")


def parseResult_stream(completions):
    result = ""
    for chunk in completions:
        chunk_message = chunk['choices'][0]['delta']
        res = chunk_message.get('content', '')
        Log.answer(res, end='')
        result += res
    Log.answer('\n')
    Log.info("Finish")
    messages.append({"role": "assistant", "content": result})


def initOpenAI():
    global messages
    openai.organization = "org-nQ2su19ado3KvvI9HE5vAZHO"
    openai.api_key = os.getenv("OPENAI_API_KEY")
    messages.append({"role": "system", "content": "You are a helpful assistant."})


def chat():
    global messages, stream
    initOpenAI()
    Log.point("Start Chatting")
    while True:
        content = input()
        if content == "quit":
            save()
            break
        messages.append({"role": "user", "content": content})

        try:
            parseResult_stream(generateCompletion(messages)) if stream else parseResult(generateCompletion(messages))
        except APIConnectionError:
            Log.error("[APIConnectionError]:Connection timed out. Please check the network or try again later")
        except InvalidRequestError:
            Log.error("[InvalidRequestError]:Possibly because the input token exceeds the maximum limit")


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
