import logging
import threading
import traceback

from bFdcAPI.MCP.Dto.FdcMcpEvent import FdcMcpEventResDto
from bFdcAPI.MCP.UseCase import FdcMcpUseCase
from bFdcAPI.Enum import RecvState
from fdcmp.Value import LogicItem


class MCPEqpEvent:
    def __init__(self, resDto: FdcMcpEventResDto) -> None:
        self.id = resDto.id
        self.name = resDto.name
        self.eventCode = resDto.eventCode
        self.eqp = resDto.eqp
        self.__eqpModule = resDto.eqpModule
        self.__resDto = resDto
        self.__fdcMcpUseCase = FdcMcpUseCase()
        self.__logicsRecvState = RecvState.init
        self.__logics: list[LogicItem] = list()
        self.__loggerMcp = logging.getLogger("mcp")
        self.__logicsLock = threading.Lock()

    def getLogics(self, event: int) -> list[LogicItem]:
        try:
            self.__logicsLock.acquire()
            if self.__logicsRecvState == RecvState.init:
                for eventLV in self.__fdcMcpUseCase.getEventLVList(event):
                    if eventLV.logicCode is not None:
                        com = compile(eventLV.logicCode, '<string>', mode='exec')
                        self.__logics.append(LogicItem(eventLV.name, com))
                self.__logicsRecvState = RecvState.done
        except Exception as e:
            self.__loggerMcp.error(e.__str__())
            self.__loggerMcp.error(traceback.print_stack())
            self.__logicsRecvState = RecvState.error
        finally:
            self.__logicsLock.release()

        return self.__logics
