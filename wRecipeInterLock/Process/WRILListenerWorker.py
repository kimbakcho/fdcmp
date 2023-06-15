from multiprocessing import Queue

from ESB.ListenerWorker import ListenerWorker


class WRILListenerWorker(ListenerWorker):
    def __init__(self) -> None:
        super().__init__()
        self.q = Queue()
        self.c = Queue()

    def onMessage(self, message: str):
        self.q.put(message)

    def onCommandMessage(self, message: str):
        self.c.put(message)
