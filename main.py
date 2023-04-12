from lib.Log import Log
from lib.ClIHandle import ClIHandle
from lib.options import *
import asyncio


async def run():
    cli = ClIHandle()
    cli.add("chat", chat)
    cli.add("set", selectChat)
    cli.add("all", allChats)
    cli.add("save", save)
    cli.add("i", image)
    cli.add("t", translate)
    while True:
        Log.point("Action")

        user_input = input()
        split_input = user_input.split()
        option = split_input[0]
        args = split_input[1:]

        if option == "quit":
            break
        await cli.parse(option, *args)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())