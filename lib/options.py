import datetime
import glob

from Log import *
import json
import os
import asyncio
import aiofiles

messages: list[dict] = []
current_file_name: str = ""


def generateCatalogue(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def getChatLogsPath():
    doc_path = os.path.join(os.path.expanduser("~"), "Documents")
    return os.path.join(doc_path, "chat_logs")


async def write(msg: list[dict], fp):
    for item in msg:
        json.dump(item, fp)
        await fp.write('\n')


async def save(fp=None):
    global messages, current_file_name
    fileName = datetime.datetime.now().strftime(
        "%Y-%m-%d-%H-%M-%S") + ".json" if current_file_name == "" else current_file_name
    current_file_name = fileName
    filePath = getChatLogsPath()
    Log.info("Saving File {}".format(fileName))
    if fp is not None:
        await write(messages, fp)
    else:
        async with aiofiles.open(os.path.join(filePath, fileName), 'a') as fp:
            await write(messages, fp)
    Log.info("Saved File {}".format(fileName))


# noinspection PyTypeChecker
async def setCurrentFile(fileName: str):
    global current_file_name, messages
    filePath = getChatLogsPath()
    try:
        async with aiofiles.open(os.path.join(filePath, fileName), 'r') as fp:
            messages.clear()
            current_file_name = fileName
            async for line in fp:
                item = json.loads(line)
                messages.append(item)
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


Log.info("File Directory Generating")
chat_logs_path = getChatLogsPath()
generateCatalogue(getChatLogsPath())
Log.info("File Directory Generated. Located at {}".format(chat_logs_path))

__all__ = [
    "save",
    "selectChat",
    "allChats"
]
