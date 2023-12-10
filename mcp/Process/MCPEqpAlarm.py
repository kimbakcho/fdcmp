import logging
import traceback
from typing import List, Dict

from FDCContext.logicConverter import decoratorLogicCode
from bFdcAPI.MCP.Dto.FdcMcpAlarm import FdcMcpAlarmResDto
from bFdcAPI.MCP.Dto.FdcMcpAlarmLV import FdcMcpAlarmLVResDto
from bFdcAPI.MCP.UseCase import FdcMcpUseCase
from bFdcAPI.Enum import RecvState
from fdcmp.Value import LogicItem


class MCPEqpAlarm:
    def __init__(self, resDto: FdcMcpAlarmResDto) -> None:
        self.id = resDto.id
        self.name = resDto.name
        self.alarmCode = resDto.alarmCode
        self.eqp = resDto.eqp
        self.__eqpModule = resDto.eqpModule
        self.__resDto = resDto
        self.__fdcMcpUseCase = FdcMcpUseCase()
        self.__logicsRecvState = RecvState.init
        self.__logics: list[LogicItem] = list()
        self.__alarmLVs: dict[str, FdcMcpAlarmLVResDto] = dict()
        self.__loggerMcp = logging.getLogger("mcp")

    def getLogics(self, alarm: int) -> List[LogicItem]:
        try:
            if self.__logicsRecvState in [RecvState.init, RecvState.needReload, RecvState.error]:
                self.__logics = list()
                self.__alarmLVs = dict[str, FdcMcpAlarmLVResDto]()
                for alarmLV in self.__fdcMcpUseCase.getAlarmLVList(alarm):
                    if alarmLV.logicCode is not None:
                        com = compile(decoratorLogicCode(alarmLV.logicCode), '<string>', mode='exec')
                        self.__logics.append(LogicItem(alarmLV.name, com))
                        self.__alarmLVs[alarmLV.name] = alarmLV
                self.__logicsRecvState = RecvState.done
        except Exception as e:
            self.__loggerMcp.error(e.__str__())
            self.__loggerMcp.error(traceback.print_stack())
            self.__logicsRecvState = RecvState.error

        return self.__logics

    def getAlarmLVs(self) -> Dict[str, FdcMcpAlarmLVResDto]:
        return self.__alarmLVs

    def setAlarmLVAPIRecvState(self, state: RecvState):
        self.__logicsRecvState = state
