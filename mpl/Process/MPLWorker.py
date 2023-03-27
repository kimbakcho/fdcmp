import json
import multiprocessing
import threading
import traceback

from bFdcAPI.Eqp.Dto.FdcEqpModule import FdcEqpModuleReqDto
from bFdcAPI.Eqp.UseCase import FdcEqpUseCase
from fdcmp.settings import BASE_DIR, env
from multiprocessing import Queue
from FDCContext.context import Context
from mcp.Process.MCPEqpModule import MCPEqpModule
from mcp.Process.MCPThreadWorker import mcpWorker

from mpl.Process.MPLParserUtil import MPLParserUtil

import logging
class MPLWorker:
    def __init__(self, moduleId: int, q: Queue, c: Queue) -> None:
        self.q = q
        self.c = c
        self.moduleId = moduleId
        self.__loggerMpl = logging.getLogger('mpl')
        self.__mplParserUtil = MPLParserUtil()
        self.__eqpUseCase = FdcEqpUseCase()
        module = self.__eqpUseCase.getEqpModule(id=self.moduleId)
        self.__module = MCPEqpModule(module)
        self.__context = Context()


    def messageParser(self, message: str):
        try:
            self.__context.set_message(message)
            for logicItem in self.__mplParserUtil.getMpLogics():
                exec(logicItem.logicComPile, None, locals())
                runResult = locals().get("run")(self.__context)
                self.__context.mp[logicItem.name] = runResult
            mcpWorker(self.__module, self.__context)
            self.__context.set_message(message)
        except Exception as e:
            self.__loggerMpl.error(e.__str__())
            self.__loggerMpl.error(traceback.print_stack())

    def commandParser(self, message: str):
        message = json.loads(message)
        pass
        # if message['command'] == SystemCommand.systemInit.value:
