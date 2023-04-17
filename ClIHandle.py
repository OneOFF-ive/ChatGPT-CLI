from Log import Log


class ClIHandle:

    def __init__(self):
        self.name2Func = {}

    def add(self, name: str, func):
        self.name2Func[name] = func

    def delete(self, name: str):
        return self.name2Func.pop(name)

    async def parse(self, name: str, *args):
        function = self.name2Func.get(name)
        if function is not None:
            await function(*args)
        else:
            Log.error("Option Does Not Exist")
