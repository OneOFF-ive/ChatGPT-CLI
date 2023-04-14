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
    def answer(message, end='\n'):
        print(Fore.LIGHTBLUE_EX + message + "\033[0m", end=end)

    @staticmethod
    def error(message, error="Error"):
        print(Fore.LIGHTRED_EX + "[{}]:".format(error) + message + "\033[0m")

    @staticmethod
    def warn(message):
        print(Fore.RED + "[warn]:" + message + "\033[0m")


__all__ = [
    "Log"
]
