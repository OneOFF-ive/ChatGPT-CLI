from typing import Dict, Callable


class CliHandle:

    def __init__(self):
        self.name2Func: Dict[str, Callable[[], None]] = {}

    def add(self, name: str, func: Callable[[], None]):
        self.name2Func[name] = func

    def delete(self, name: str):
        return self.name2Func.pop(name)

    def parse(self, name: str):
        function: Callable[[], None] = self.name2Func.get(name);
        if function is not None:
            function()


cli = CliHandle()
cli.add("test", lambda: print("test"))
cli.parse("test")
