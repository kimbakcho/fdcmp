import json
import traceback

from bFdcAPI.Enum import CommandType, CommandModule, CommandAction, RecvState
from bFdcAPI.Eqp.UseCase import FdcEqpUseCase
from multiprocessing import Queue
from FDCContext.context import Context
from mpl.Process.MPLParserUtil import MPLParserUtil

import logging
class MPLWorker:
    def __init__(self, moduleId: int, q: Queue, c: Queue) -> None:
        from mcp.Process.MCPEqpModule import MCPEqpModule
        from mcp.Process.MCPWorker import McpWorker
        self.q = q
        self.c = c
        self.moduleId = moduleId
        self.__loggerMpl = logging.getLogger('mpl')
        self.__mplParserUtil = MPLParserUtil()
        self.__eqpUseCase = FdcEqpUseCase()
        module = self.__eqpUseCase.getEqpModule(id=self.moduleId)
        self.__module = MCPEqpModule(module)
        self.__context = Context()
        self.__mcpWorker = McpWorker()

    def messageParser(self, message: str):
        try:
            self.__context.set_message(message)
            for logicItem in self.__mplParserUtil.getMpLogics():
                exec(logicItem.logicComPile, None, locals())
                runResult = locals().get("run")(self.__context)
                self.__context.mp[logicItem.name] = runResult
            self.__mcpWorker.run(self.__module, self.__context)
        except Exception as e:
            self.__loggerMpl.error(e.__str__())
            self.__loggerMpl.error(traceback.format_stack())
            traceback.print_stack()

    def commandParser(self, message: str):
        r = json.loads(message)
        if r.get("Module") == CommandModule.mcp.value:
            if r.get("Type") == CommandType.event.value:
                if r.get("Action") == CommandAction.create.value:
                    self.__module.setEventAPIRecvState(RecvState.apiCreated)

        # if message['command'] == SystemCommand.systemInit.value:
