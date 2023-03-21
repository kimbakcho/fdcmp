import json
import multiprocessing

from environ import environ

from bFdc.Eqp.UseCase import FdcEqpUseCase
from bFdc.MP.UseCase import FdcMpUseCase

from fdcmp.settings import BASE_DIR, env
from multiprocessing import Queue
from FDCContext.context import Context

from mpl.Process.MPLParserUtil import MPLParserUtil


class MPLWorker:
    def __init__(self, q: Queue, c: Queue, mplParserUtil: MPLParserUtil) -> None:
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
        self.mplParserUtil = mplParserUtil

    def messageParser(self, message: str):
        for logicItem in self.mplParserUtil.getMpLogics():
            if logicItem["compile"] is not None:
                exec(logicItem["compile"], None, locals())
                runResult = locals().get("run")(self.context)
                self.context.mp[logicItem['name']] = runResult
                print(f'{multiprocessing.current_process().name} {self.context.mp["EqpCode"]}')

        if self.mplParserUtil.getEqps().keys() in self.context.mp["EqpCode"]:
            eqp = self.mplParserUtil.getEqps().get(self.context.mp["EqpCode"])
            eqp.getModule()
            pass


    def commandParser(self, message: str):
        message = json.loads(message)
        pass
        # if message['command'] == SystemCommand.systemInit.value:
