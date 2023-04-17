import asyncio
import datetime
import glob
import json
import aiofiles
from openai.error import APIConnectionError, InvalidRequestError

from ApiBuilder import *

messages: list[dict] = [{"role": "system", "content": "You are a helpful assistant."}]
current_file_name: str = ""
events_loop = asyncio.get_event_loop()


def generateCatalogue(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def getChatLogsPath():
    doc_path = os.path.join(os.path.expanduser("~"), "Documents")
    return os.path.join(doc_path, "chat_logs")


def getCurrentFileName():
    global current_file_name
    fileName = datetime.datetime.now().strftime(
        "%Y-%m-%d-%H-%M-%S") + ".json" if current_file_name == "" else current_file_name
    current_file_name = fileName
    return fileName


async def openCurrentFileBy(mode):
    fileName = getCurrentFileName()
    filePath = getChatLogsPath()
    file = await aiofiles.open(os.path.join(filePath, fileName), mode)
    if os.path.getsize(os.path.join(filePath, fileName)) == 0 and mode != 'r':
        await file.write(json.dumps(messages[0]) + '\n')
    return file


async def write(msg: list[dict], fp):
    for item in msg:
        data2json = json.dumps(item) + '\n'
        await fp.write(data2json)


async def save(fp=None):
    global messages, current_file_name
    fileName = getCurrentFileName()
    Log.info("Saving File {}".format(fileName))
    if fp is not None:
        await write(messages, fp)
    else:
        fp = await openCurrentFileBy('w')
        await write(messages, fp)
        await fp.close()
    Log.info("Saved File {}".format(fileName))


async def append(msg: list[dict], fp=None):
    global current_file_name
    if fp is not None:
        await write(messages, fp)
    else:
        fp = await openCurrentFileBy('a')
        await write(msg, fp)
        await fp.close()


# noinspection PyTypeChecker
async def setCurrentFile(fileName: str):
    global current_file_name, messages
    try:
        fp = await openCurrentFileBy('r')
        messages.clear()
        current_file_name = fileName
        async for line in fp:
            item = json.loads(line)
            messages.append(item)
        await fp.close()
    except FileNotFoundError as e:
        raise e


async def allChats():
    filePath = getChatLogsPath()
    Log.point("Existing Files：")
    for file in glob.glob(os.path.join(filePath, "*.json")):
        Log.answer(file)


async def selectChat(fileName):
    global messages
    try:
        Log.info("Loading File {}".format(fileName))
        await setCurrentFile(fileName)
        Log.info("Loaded File {}, Messages Is {}".format(fileName, messages))
    except FileNotFoundError:
        Log.error("File Does Not Exist")


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


async def chat():
    global messages
    filePath = getChatLogsPath()
    fileName = getCurrentFileName()
    Log.info("File Name: {}".format(os.path.join(filePath, fileName)))
    Log.point("Start Chatting")

    while True:
        content = await asyncio.get_running_loop().run_in_executor(None, input, '')
        if content == "quit":
            await save()
            break
        messages.append({"role": "user", "content": content})

        try:
            res = ApiBuilder.ChatCompletion(messages)
            parseResult_stream(res) if default_config.chatCompletionConfig.stream else parseResult(res)
            asyncio.create_task(append(messages[-2:]))
        except APIConnectionError:
            Log.error("[APIConnectionError]:Connection timed out. Please check the network or try again later")
        except InvalidRequestError:
            Log.error("[InvalidRequestError]:Possibly because the input token exceeds the maximum limit")


Log.info("File Directory Generating")
chat_logs_path = getChatLogsPath()
generateCatalogue(getChatLogsPath())
Log.info("File Directory Generated. Located at {}".format(chat_logs_path))

__all__ = [
    "save",
    "selectChat",
    "allChats",
    "chat"
]
