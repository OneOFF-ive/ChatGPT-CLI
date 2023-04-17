import os

from colorama import Fore

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

    os.system('cls' if os.name == 'nt' else 'clear')
    root_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(root_path, "logo.txt"), 'r') as file:
        logo = file.read()
    print(Fore.CYAN + logo)

    while True:
        Log.point("Next")

        user_input = input()
        user_input = user_input.strip()
        split_input = user_input.split()
        option = split_input[0]
        args = split_input[1:]

        if option == "quit":
            break
        await cli.parse(option, *args)


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
