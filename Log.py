class Log:
    @staticmethod
    def info(message):
        print("\033[92m" + "[info]:" + message + "\033[0m")

    @staticmethod
    def point(message):
        print("\033[93m" + message + "\033[0m")

    @staticmethod
    def answer(message):
        print("\033[94m" + message + "\033[0m")

    @staticmethod
    def error(message):
        print("\033[91m" + "[error]:" + message + "\033[0m")
