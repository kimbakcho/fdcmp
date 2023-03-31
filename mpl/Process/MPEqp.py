import traceback

from bFdcAPI.Enum import RecvState
from bFdcAPI.Eqp.Dto.FdcEqp import FdcEqpResDto
from bFdcAPI.Eqp.Dto.FdcEqpModule import FdcEqpModuleReqDto
from bFdcAPI.Eqp.UseCase import FdcEqpUseCase
import logging

from mpl.Process.MPEqpModule import MPEqpModule


class MPEqp:
    def __init__(self, resDto: FdcEqpResDto) -> None:
        self.name = resDto.name
        self.code = resDto.code
        self.id = resDto.id
        self.__resDto = resDto
        self.__modules: list[MPEqpModule] = list()
        self.__moduleRecv = RecvState.init
        self.__eqpUseCase = FdcEqpUseCase()
        self.__loggerMpl = logging.getLogger('mpl')

    def getModules(self) -> list[MPEqpModule]:
        try:
            if self.__moduleRecv == RecvState.init:
                modules = self.__eqpUseCase.getEqpModuleList(FdcEqpModuleReqDto(eqp=self.id))
                for module in modules:
                    self.__modules.append(MPEqpModule(module))
                self.__moduleRecv = RecvState.done
        except Exception as e:
            self.__loggerMpl.error(e.__str__())
            self.__loggerMpl.error(traceback.format_stack())
            traceback.print_stack()
            self.__moduleRecv = RecvState.error
        return self.__modules

    def getModule(self, id: int) -> MPEqpModule | None:
        try:
            for module in self.__modules:
                if module.id == id:
                    return module
        except Exception as e:
            self.__loggerMpl.error(e.__str__())
            self.__loggerMpl.error(traceback.format_stack())
            traceback.print_stack()

    def addModule(self, mpEqpModule: MPEqpModule):
        self.__modules.append(mpEqpModule)

    def removeModule(self, id: int):
        for (index, module) in enumerate(self.__modules):
            if module.id == id:
                self.__modules.pop(index)
