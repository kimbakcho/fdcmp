import threading
import traceback
from typing import List

from bFdcAPI.Eqp.Dto.FdcEqp import FdcEqpResDto
from bFdcAPI.Eqp.Dto.FdcEqpModule import FdcEqpModuleReqDto
from bFdcAPI.Eqp.UseCase import FdcEqpUseCase
from mcp.Process.MCPEqpModule import MCPEqpModule
from bFdcAPI.Enum import RecvState
import logging


class MPLEqp:
    def __init__(self, resDto: FdcEqpResDto) -> None:
        self.name = resDto.name
        self.code = resDto.code
        self.id = resDto.id
        self.__resDto = resDto
        self.__modules = []
        self.__moduleRecv = RecvState.init
        self.__moduleLock = threading.Lock()
        self.__loggerMpl = logging.getLogger('mpl')

    def getModule(self) -> List[MCPEqpModule]:
        try:
            self.__moduleLock.acquire()
            if self.__moduleRecv == RecvState.init:
                modules = FdcEqpUseCase.getEqpModuleList(FdcEqpModuleReqDto(eqp=self.id))
                self.__modules = list(
                    map(lambda x: MCPEqpModule(x), modules)
                )
                self.__moduleRecv = RecvState.done
        except Exception as e:
            self.__loggerMpl.error(e.__str__())
            self.__loggerMpl.error(traceback.print_stack())
            self.__moduleRecv = RecvState.error
        finally:
            self.__moduleLock.release()
        return self.__modules
