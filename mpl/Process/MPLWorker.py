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
                if r.get("Action") in [CommandAction.create.value, CommandAction.update.value,
                                       CommandAction.delete.value, CommandAction.orderSwap.value]:
                    self.__module.setEventAPIRecvState(RecvState.needReload)
            elif r.get("Type") == CommandType.eventlv.value:
                if r.get("Action") in [CommandAction.create.value, CommandAction.update.value,
                                       CommandAction.delete.value, CommandAction.orderSwap.value]:
                    if r.get("EventCode") in self.__module.getEvents().keys():
                        self.__module.getEvents()[r.get("EventCode")].setEventLVAPIRecvState(RecvState.needReload)
            elif r.get("Type") == CommandType.conditions.value:
                if r.get("Action") in [CommandAction.create.value, CommandAction.update.value,
                                       CommandAction.delete.value, CommandAction.orderSwap.value]:
                    self.__module.setConditionsAPIRecvState(RecvState.needReload)
            elif r.get("Type") == CommandType.traceGroup.value:
                if r.get("Action") in [CommandAction.create.value, CommandAction.update.value,
                                       CommandAction.delete.value, CommandAction.orderSwap.value]:
                    self.__module.setTraceGroupAPIRecvState(RecvState.needReload)
            elif r.get("Type") == CommandType.tracelv.value:
                if r.get("Action") in [CommandAction.create.value, CommandAction.update.value,
                                       CommandAction.delete.value, CommandAction.orderSwap.value]:
                    if r.get("TraceGroup") in self.__module.getTraceGroup().keys():
                        self.__module.getTraceGroup()[r.get("TraceGroup")].setTraceLVAPIRecvState(RecvState.needReload)
        elif r.get("Module") == CommandModule.mpl.value:
            if r.get("Type") == CommandType.mpLogic.value:
                if r.get("Action") in [CommandAction.create.value, CommandAction.update.value,
                                       CommandAction.delete.value, CommandAction.orderSwap.value]:
                    self.__mplParserUtil.setMPLogicAPIRecvState(RecvState.needReload)

