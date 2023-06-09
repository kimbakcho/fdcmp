import logging
import traceback
from typing import List, Optional

from bFdcAPI.Enum import RecvState, EqpModuleType
from bFdcAPI.Eqp.Dto.FdcEqp import FdcEqpResDto
from bFdcAPI.Eqp.Dto.FdcEqpModule import FdcEqpModuleReqDto
from bFdcAPI.Eqp.UseCase import FdcEqpUseCase
from capa.Process.CapaEqpModule import CapaEqpModule
from mpl.Process.MPEqpModule import MPEqpModule


class CapaEqp:

    def __init__(self, resDto: FdcEqpResDto) -> None:
        self.name = resDto.name
        self.code = resDto.code
        self.id = resDto.id
        self.__resDto = resDto
        self.__modules: list[CapaEqpModule] = list()
        self.__moduleRecv = RecvState.init

        self.__loggerMpl = logging.getLogger('capa')

    def getModules(self) -> List[CapaEqpModule]:
        try:
            if self.__moduleRecv == RecvState.init:
                modules = FdcEqpUseCase.getEqpModuleList(FdcEqpModuleReqDto(eqp=self.id))
                for module in modules:
                    if module.moduleType == EqpModuleType.capa.value:
                        self.__modules.append(CapaEqpModule(module))
                self.__moduleRecv = RecvState.done
        except Exception as e:
            self.__loggerMpl.error(traceback.format_exc())
            self.__loggerMpl.error(e.__str__())
            self.__loggerMpl.error(traceback.format_stack())
            traceback.print_stack()
            self.__moduleRecv = RecvState.error
        return self.__modules

    def getModule(self, id: int) -> Optional[CapaEqpModule]:
        try:
            for module in self.__modules:
                if module.id == id:
                    return module
        except Exception as e:
            self.__loggerMpl.error(traceback.format_exc())
            self.__loggerMpl.error(e.__str__())
            self.__loggerMpl.error(traceback.format_stack())
            traceback.print_stack()

    def addModule(self, capaEqpModule: CapaEqpModule):
        self.__modules.append(capaEqpModule)

    def removeModule(self, id: int):
        for (index, module) in enumerate(self.__modules):
            if module.id == id:
                self.__modules.pop(index)