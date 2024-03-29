import json
import traceback

from FDCContext.logicConverter import decoratorLogicCode
from bFdcAPI.ACP.UseCase import ACPUseCase
from bFdcAPI.Enum import CommandType, CommandModule, CommandAction, RecvState
from bFdcAPI.Eqp.UseCase import FdcEqpUseCase
from multiprocessing import Queue
from FDCContext.context import Context, OperationAPIModule, CapaAPIModule
from bFdcAPI.MCP.UseCase import FdcMcpUseCase
from mpl.Process.MPLParserUtil import MPLParserUtil

import logging


class MPLWorker:
    def __init__(self, moduleId: int, q: Queue, c: Queue) -> None:
        self.q = q
        self.c = c
        self.moduleId = moduleId
        self.__loggerMpl = logging.getLogger('mpl')
        self.moduleInit()

    def moduleInit(self):
        from mcp.Process.MCPEqpModule import MCPEqpModule
        from mcp.Process.MCPWorker import McpWorker
        self.__mplParserUtil = MPLParserUtil()

        module = FdcEqpUseCase.getEqpModule(id=self.moduleId)
        self.moduleObj = module
        self.__module = MCPEqpModule(module)
        self.__context = Context()
        self.__context.setEqpCode(self.__module.eqpCode)
        self.__context.setEqpName(self.__module.eqpName)
        self.__context.setModuleCode(self.__module.code)
        self.__context.setModuleName(self.__module.name)
        self.__context.setLogger(logging.getLogger("mcp"))
        self.__context.setOperationAPIModule(OperationAPIModule(self.__module.id))
        self.__context.setCapaAPIModule(CapaAPIModule(self.__module.id))
        self.initRun()
        self.__mcpWorker = McpWorker(self.__context,self.__module)

    def initRun(self):
        inits = FdcMcpUseCase.getInitList(eqpModule=self.moduleId)
        for init in inits:
            if init.get("logicCode"):
                try:
                    com = compile(decoratorLogicCode(init.get("logicCode")), '<string>', mode='exec')
                    exec(com, None, locals())
                    locals().get("run")(self.__context)
                except Exception as e:
                    self.__loggerMpl.error(f'{self.__module.eqpName}_{self.__module.name} {init.get("name")}')
                    self.__loggerMpl.error(traceback.format_exc())
                    self.__loggerMpl.error(e.__str__())
                    self.__loggerMpl.error(traceback.format_stack())
                    traceback.print_stack()

    def reloadModule(self):
        del self.__mplParserUtil
        del self.__module
        del self.__context
        del self.__mcpWorker
        self.moduleInit()

    def messageParser(self, message: str):
        try:
            self.__context.set_message(message)
            self.__context.setEqpCode(self.__module.eqpCode)
            self.__context.setEqpName(self.__module.eqpName)
            self.__context.setModuleCode(self.__module.code)
            self.__context.setModuleName(self.__module.name)
            self.__context.debugMsgs.clear()
            self.__context.setSPCData(None)
            if self.moduleObj.isDebug:
                self.__loggerMpl.info("messageParser1")
                self.__loggerMpl.info(message)
            for logicItem in self.__mplParserUtil.getMpLogics():
                try:
                    if self.moduleObj.isDebug:
                        self.__loggerMpl.info("messageParser2")
                        self.__loggerMpl.info(logicItem.name)
                    exec(logicItem.logicComPile, None, locals())
                    if self.moduleObj.isDebug:
                        self.__loggerMpl.info("messageParser3")
                    runResult = locals().get("run")(self.__context)
                    self.__context.mp[logicItem.name] = runResult
                except Exception as e:
                    self.__loggerMpl.error(f'{self.__module.eqpName}_{self.__module.name} {logicItem.name}')
                    self.__loggerMpl.error(message)
                    self.__loggerMpl.error(traceback.format_exc())
                    self.__loggerMpl.error(e.__str__())
                    self.__loggerMpl.error(traceback.format_stack())
                    traceback.print_stack()
            if self.moduleObj.isDebug:
                self.__loggerMpl.info("messageParser4")
            self.__mcpWorker.run()
            if self.moduleObj.isDebug:
                self.__loggerMpl.info("messageParser5")
        except Exception as e:
            self.__loggerMpl.error(traceback.format_exc())
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
            if r.get("Type") == CommandType.alarm.value:
                if r.get("Action") in [CommandAction.create.value, CommandAction.update.value,
                                       CommandAction.delete.value, CommandAction.orderSwap.value]:
                    self.__module.setAlarmAPIRecvState(RecvState.needReload)
            elif r.get("Type") == CommandType.alarmlv.value:
                if r.get("Action") in [CommandAction.create.value, CommandAction.update.value,
                                       CommandAction.delete.value, CommandAction.orderSwap.value]:
                    if r.get("AlarmCode") in self.__module.getAlarms().keys():
                        self.__module.getAlarms()[r.get("AlarmCode")].setAlarmLVAPIRecvState(RecvState.needReload)
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
            elif r.get("Type") == CommandType.init.value:
                if r.get("Action") in [CommandAction.create.value, CommandAction.update.value,
                                       CommandAction.delete.value, CommandAction.orderSwap.value]:
                    self.initRun()
            elif r.get("Type") == CommandType.threadingLoop.value:
                if r.get("Action") in [CommandAction.create.value, CommandAction.update.value]:
                    self.__mcpWorker.createOrUpdateThreading(r.get("Id"))
                elif r.get("Action") in [CommandAction.delete.value]:
                    self.__mcpWorker.deleteThreading(r.get("Name"))

        elif r.get("Module") == CommandModule.mpl.value:
            if r.get("Type") == CommandType.mpLogic.value:
                if r.get("Action") in [CommandAction.create.value, CommandAction.update.value,
                                       CommandAction.delete.value, CommandAction.orderSwap.value]:
                    self.__mplParserUtil.setMPLogicAPIRecvState(RecvState.needReload)

        elif r.get("Module") == CommandModule.eqp.value:
            if r.get("Action") in [CommandAction.update.value]:
                self.__module.reLoadBasicInfo()
        elif r.get("Module") == CommandModule.eqpModule.value:
            if r.get("Action") in [CommandAction.update.value]:
                self.__module.reLoadBasicInfo()
            elif r.get("Action") in [CommandAction.moduleRestart.value]:
                self.reloadModule()
