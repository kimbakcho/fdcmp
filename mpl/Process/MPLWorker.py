from environ import environ

from fdcmp.settings import BASE_DIR
from multiprocessing import Queue
from FDCContext.context import Context
import requests

env = environ.Env()


class MPLWorker:
    def __init__(self, q: Queue, c: Queue) -> None:
        import logging
        self.q = q
        self.c = c
        self.loggerMpl = logging.getLogger('mpl')
        self.loggerMpl.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s')
        handler = logging.FileHandler(f'{BASE_DIR}/mpl/mplLog.log')
        handler.setFormatter(formatter)
        self.loggerMpl.addHandler(handler)
        self.context = Context()
        self.__initCompile()

    def __initCompile(self):
        self.comPilePythons = list()
        r = requests.get(f"{env('BFDC_URL')}/mp/mpl/")
        mplItems = r.json()
        for item in mplItems:
            if item["logicCode"] is not None:
                com = compile(item["logicCode"], '<string>', mode='exec')
                self.comPilePythons.append({"compilePy": com, "name": item["name"], "id": item["id"]})

    def messageParser(self, message: str):
        for logicItem in self.comPilePythons:
            com = logicItem.get("compilePy")
            exec(com, None, locals())
            runResult = locals().get("run")(self.context)
            self.context.__dict__.setdefault(logicItem.get("name"), runResult)

    def commandParser(self, message: str):
        if message is "MPLogicReload":
            self.__initCompile()


