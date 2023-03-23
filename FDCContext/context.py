class Context:
    def __init__(self, message: str | None = None) -> None:
        self.debugMsgs = []
        super().__init__()
        self.__message = message
        self.mp = {}
        self.event = {}
        self.trace = {}
        self.conditions = {}

    def get_message(self):
        return self.__message

    def set_message(self, value: str):
        self.__message = value

    def debug(self, msg: str):
        self.debugMsgs.append(msg)
