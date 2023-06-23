import threading
import traceback
from typing import List, Dict

from FDCContext.logicConverter import decoratorLogicCode
from bFdcAPI.Eqp.Dto.FdcEqpModule import FdcEqpModuleResDto
from bFdcAPI.Eqp.UseCase import FdcEqpUseCase
import logging

from bFdcAPI.MCP.UseCase import FdcMcpUseCase
from fdcmp.Value import LogicItem
from mcp.Process.MCPEqpAlarm import MCPEqpAlarm
from mcp.Process.MCPEqpEvent import MCPEqpEvent
from bFdcAPI.Enum import RecvState
from mcp.Process.MCPEqpTraceGroup import McpEqpTraceGroup


class MCPEqpModule:
    def __init__(self, resDto: FdcEqpModuleResDto) -> None:
        self.code = resDto.code
        self.name = resDto.name
        self.eqp = resDto.eqp
        self.eqpName = resDto.eqpName
        self.eqpCode = resDto.eqpCode
        self.id = resDto.id
        self.__resDto = resDto
        self.__eqpUseCase = FdcEqpUseCase()
        self.__fdcMcpUseCase = FdcMcpUseCase()
        self.__loggerMcp = logging.getLogger('mcp')
        self.__events: dict[str, MCPEqpEvent] = dict()
        self.__eventsRecvState = RecvState.init
        self.__alarms: dict[str, MCPEqpEvent] = dict()
        self.__alarmsRecvState = RecvState.init
        self.__traceGroups: dict[str, McpEqpTraceGroup] = dict()
        self.__traceGroupRecvState = RecvState.init
        self.__conditionsRecvState = RecvState.init
        self.__conditions = list()

    def setEventAPIRecvState(self, state: RecvState):
        self.__eventsRecvState = state

    def getEvents(self) -> Dict[str, MCPEqpEvent]:
        try:
            if self.__eventsRecvState in [RecvState.init, RecvState.needReload]:
                self.__events = dict[str, MCPEqpEvent]()
                for item in self.__fdcMcpUseCase.getEventList(self.id):
                    self.__events[item.eventCode] = MCPEqpEvent(item)
                self.__eventsRecvState = RecvState.done
        except Exception as e:
            self.__loggerMcp.error(e.__str__())
            self.__loggerMcp.error(traceback.print_stack())
            self.__eventsRecvState.error = RecvState.error
        return self.__events

    def getAlarms(self) -> Dict[str, MCPEqpAlarm]:
        try:
            if self.__alarmsRecvState in [RecvState.init, RecvState.needReload]:
                self.__alarms = dict[str, MCPEqpAlarm]()
                for item in self.__fdcMcpUseCase.getAlarmList(self.id):
                    self.__alarms[item.alarmCode] = MCPEqpAlarm(item)
                self.__alarmsRecvState = RecvState.done
        except Exception as e:
            self.__loggerMcp.error(e.__str__())
            self.__loggerMcp.error(traceback.print_stack())
            self.__alarmsRecvState.error = RecvState.error
        return self.__alarms

    def setAlarmAPIRecvState(self, state: RecvState):
        self.__alarmsRecvState = state

    def getTraceGroup(self) -> Dict[str, McpEqpTraceGroup]:
        try:
            if self.__traceGroupRecvState in [RecvState.init, RecvState.needReload]:
                self.__traceGroups = dict[str, McpEqpTraceGroup]()
                for item in self.__fdcMcpUseCase.getTraceGroupList(self.id):
                    self.__traceGroups[item.traceGroupCode] = McpEqpTraceGroup(item)
                self.__traceGroupRecvState = RecvState.done
        except Exception as e:
            self.__loggerMcp.error(e.__str__())
            self.__loggerMcp.error(traceback.print_stack())
        return self.__traceGroups

    def setTraceGroupAPIRecvState(self, state: RecvState):
        self.__traceGroupRecvState = state

    def getConditions(self) -> List[LogicItem]:
        try:
            if self.__conditionsRecvState in [RecvState.init, RecvState.needReload]:
                self.__conditions = list[LogicItem]()
                for conditions in self.__fdcMcpUseCase.getConditions(self.id):
                    if conditions.logicCode is not None:
                        com = compile(decoratorLogicCode(conditions.logicCode), '<string>', mode='exec')
                        self.__conditions.append(LogicItem(conditions.name, com))
                self.__conditionsRecvState = RecvState.done
        except Exception as e:
            self.__loggerMcp.error(e.__str__())
            self.__loggerMcp.error(traceback.print_stack())
            self.__conditionsRecvState = RecvState.error
        return self.__conditions

    def setConditionsAPIRecvState(self, state: RecvState):
        self.__conditionsRecvState = state

    def reLoadBasicInfo(self):
        module = FdcEqpUseCase.getEqpModule(id=self.id)
        self.code = module.code
        self.name = module.name
        self.eqp = module.eqp
        self.eqpName = module.eqpName
        self.eqpCode = module.eqpCode
        self.__resDto = module
