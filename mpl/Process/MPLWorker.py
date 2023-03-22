import json
import multiprocessing
import threading
import traceback

from fdcmp.settings import BASE_DIR, env
from multiprocessing import Queue
from FDCContext.context import Context

from mcp.Process.MCPThreadWorker import mcpThreadWorker
from mpl.Process.MPLParserUtil import MPLParserUtil
from concurrent.futures import ThreadPoolExecutor


class MPLWorker:
    def __init__(self, q: Queue, c: Queue) -> None:
        import logging
        self.q = q
        self.c = c
        self.__loggerMpl = logging.getLogger('mpl')
        self.__mplParserUtil = MPLParserUtil()
        self.__mplThreadPool = ThreadPoolExecutor(max_workers=env("MPL_TH_WORKER", int))
        self.__mcpThreadPool = ThreadPoolExecutor(max_workers=env("MCP_TH_WORKER", int))

    @staticmethod
    def mplMPThRun(message: str, mplParserUtil: MPLParserUtil, mcpThreadPool: ThreadPoolExecutor, logger):
        try:
            context = Context()
            context.set_message(message)
            for logicItem in mplParserUtil.getMpLogics():
                exec(logicItem.logicComPile, None, locals())
                runResult = locals().get("run")(context)
                context.mp[logicItem.name] = runResult
            print(f'{multiprocessing.current_process().name} {context.mp["EqpCode"]}')

            if context.mp["EqpCode"] in mplParserUtil.getEqps().keys():
                eqp = mplParserUtil.getEqps().get(context.mp["EqpCode"])
                modules = eqp.getModule()
                for module in modules:
                    mcpThreadPool.submit(mcpThreadWorker, module, context)
        except Exception as e:
            logger.error(e.__str__())
            logger.error(traceback.print_stack())

    def messageParser(self, message: str):
        self.__mplThreadPool.submit(self.mplMPThRun, message, self.__mplParserUtil, self.__mcpThreadPool,
                                    self.__loggerMpl)

    def commandParser(self, message: str):
        message = json.loads(message)
        pass
        # if message['command'] == SystemCommand.systemInit.value:
