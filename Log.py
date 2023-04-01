from colorama import init, Fore

init(autoreset=True)


class Log:
    @staticmethod
    def info(message):
        print(Fore.GREEN + "[info]:" + message + "\033[0m")

    @staticmethod
    def point(message):
        print(Fore.YELLOW + message + "\033[0m")

    @staticmethod
    def answer(message):
        print(Fore.BLUE + message + "\033[0m")

    @staticmethod
    def error(message):
        print(Fore.RED + "[error]:" + message + "\033[0m")
