import threading
import traceback

from bFdcAPI.MCP.Dto.FdcMcpTraceGroup import FdcMcpTraceGroupResDto
from bFdcAPI.MCP.UseCase import FdcMcpUseCase
from bFdcAPI.Enum import RecvState
from fdcmp.Value import LogicItem

import logging


class McpEqpTraceGroup:
    def __init__(self, resDto: FdcMcpTraceGroupResDto) -> None:
        self.id = resDto.id
        self.name = resDto.name
        self.traceGroupCode = resDto.traceGroupCode
        self.eqpModule = resDto.eqpModule
        self.__resDto = resDto
        self.__traceLVRecvState = RecvState.init
        self.__traceLVLock = threading.Lock()
        self.__mcpUseCase = FdcMcpUseCase()
        self.__logicItems: list[LogicItem] = list()
        self.__loggerMcp = logging.getLogger('mcp')

    def getTraceLogic(self):
        try:
            if self.__traceLVRecvState in [RecvState.init, RecvState.needReload]:
                __logicItems = list[LogicItem]()
                for traceLV in self.__mcpUseCase.getTraceLVList(self.id):
                    if traceLV.logicCode is not None:
                        com = compile(traceLV.logicCode, '<string>', mode='exec')
                        self.__logicItems.append(LogicItem(traceLV.name, com))
                self.__traceLVRecvState = RecvState.done
        except Exception as e:
            self.__loggerMcp.error(e.__str__())
            self.__loggerMcp.error(traceback.print_stack())
            self.__traceLVRecvState = RecvState.error

        return self.__logicItems

    def setTraceLVAPIRecvState(self, state: RecvState):
        self.__traceLVRecvState = state
