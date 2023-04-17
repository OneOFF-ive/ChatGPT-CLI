import datetime

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


async def save():
    global messages, current_file_name
    fileName = datetime.datetime.now().strftime(
        "%Y-%m-%d-%H-%M-%S") + ".json" if current_file_name == "" else current_file_name
    current_file_name = fileName
    filePath = getChatLogsPath()
    Log.info("Saving File {}".format(fileName))
    async with aiofiles.open(os.path.join(filePath, fileName), 'w') as fp:
        await write(messages, fp)
    Log.info("Saved File {}".format(fileName))


# noinspection PyTypeChecker
async def setCurrentFile(fileName: str):
    global current_file_name
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




chat_logs_path = getChatLogsPath()
generateCatalogue(chat_logs_path)
file = aiofiles.open(os.path.join(chat_logs_path, "2023-04-16-19-12-44.json"))

__all__ = [
    "save",
]
