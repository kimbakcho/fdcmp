import threading
import traceback

from bFdc.Eqp.Dto.FdcEqpModule import FdcEqpModuleResDto
from bFdc.Eqp.UseCase import FdcEqpUseCase
import logging

from bFdc.MCP.Dto.FdcMcpConditions import ConditionsResDto
from bFdc.MCP.UseCase import FdcMcpUseCase
from fdcmp.Value import LogicItem
from mcp.Process.MCPEqpEvent import MCPEqpEvent
from fdcmp.Enum import RecvState
from mcp.Process.McpEqpTraceGroup import McpEqpTraceGroup


class MCPEqpModule:
    def __init__(self, resDto: FdcEqpModuleResDto) -> None:
        self.code = resDto.code
        self.name = resDto.name
        self.eqp = resDto.eqp
        self.id = resDto.id
        self.__resDto = resDto
        self.__eqpUseCase = FdcEqpUseCase()
        self.__fdcMcpUseCase = FdcMcpUseCase()
        self.__loggerMcp = logging.getLogger('mcp')
        self.__events: dict[str, MCPEqpEvent] = dict()
        self.__eventsRecvState = RecvState.init
        self.__eventsLock = threading.Lock()
        self.__traceGroups: dict[str, McpEqpTraceGroup] = dict()
        self.__traceGroupRecvState = RecvState.init
        self.__traceGroupLock = threading.Lock()
        self.__conditionsRecvState = RecvState.init
        self.__conditionsGroupLock = threading.Lock()
        self.__conditions = list()

    def getEvents(self) -> dict[str, MCPEqpEvent]:
        try:
            self.__eventsLock.acquire()
            if self.__eventsRecvState == RecvState.init:
                for item in self.__fdcMcpUseCase.getEventList(self.id):
                    self.__events[item.eventCode] = MCPEqpEvent(item)
                self.__eventsRecvState = RecvState.done
        except Exception as e:
            self.__loggerMcp.error(e.__str__())
            self.__loggerMcp.error(traceback.print_stack())
            self.__eventsRecvState.error = RecvState.error
        finally:
            self.__eventsLock.release()
        return self.__events

    def getTraceGroup(self) -> dict[str, McpEqpTraceGroup]:
        try:
            self.__traceGroupLock.acquire()
            if self.__traceGroupRecvState == RecvState.init:
                for item in self.__fdcMcpUseCase.getTraceGroupList(self.id):
                    self.__traceGroups[item.traceGroupCode] = McpEqpTraceGroup(item)
                self.__eventsRecvState = RecvState.done
        except Exception as e:
            self.__loggerMcp.error(e.__str__())
            self.__loggerMcp.error(traceback.print_stack())
        finally:
            self.__traceGroupLock.release()
        return self.__traceGroups

    def getConditions(self) -> list[LogicItem]:
        try:
            self.__conditionsGroupLock.acquire()
            if self.__conditionsRecvState == RecvState.init:
                for conditions in self.__fdcMcpUseCase.getConditions(self.id):
                    if conditions.logicCode is not None:
                        com = compile(conditions.logicCode, '<string>', mode='exec')
                        self.__conditions.append(LogicItem(conditions.name, com))
                self.__conditionsRecvState = RecvState.done
        except Exception as e:
            self.__loggerMcp.error(e.__str__())
            self.__loggerMcp.error(traceback.print_stack())
            self.__conditionsRecvState = RecvState.error
        finally:
            self.__conditionsGroupLock.release()

        return self.__conditions
