import logging
import traceback
from typing import List, Dict

from FDCContext.logicConverter import decoratorLogicCode
from bFdcAPI.Eqp.Dto.FdcEqp import FdcEqpReqDto
from bFdcAPI.Eqp.UseCase import FdcEqpUseCase
from bFdcAPI.MP.UseCase import FdcMpUseCase
from fdcmp.Value import LogicItem
from fdcmp.settings import env
from mpl.Process.MPLEqp import MPLEqp
from bFdcAPI.Enum import RecvState


class MPLParserUtil:
    def __init__(self) -> None:
        super().__init__()
        self.__mpLogics: List[LogicItem] = list()
        # self.__eqp: Dict[str, MPLEqp] = dict()
        self.__mpUseCase = FdcMpUseCase()
        # self.__eqpUseCase = FdcEqpUseCase()
        self.__MPLogicRecvState = RecvState.init
        # self.__eqpsGetState = RecvState.init
        self.__logger = logging.getLogger("mpl")

    def getMpLogics(self) -> List[LogicItem]:
        try:
            if self.__MPLogicRecvState in [RecvState.init, RecvState.needReload]:
                self.__mpLogics = list[LogicItem]()
                for mpl in self.__mpUseCase.getMPL():
                    if mpl.logicCode is not None:
                        com = compile(decoratorLogicCode(mpl.logicCode), '<string>', mode='exec')
                        self.__mpLogics.append(LogicItem(mpl.name, com))
                self.__MPLogicRecvState = RecvState.done
        except Exception as e:
            self.__logger.error(e.__str__())
            self.__logger.error(traceback.format_stack())
            traceback.print_stack()
            self.__MPLogicRecvState = RecvState.error
        return self.__mpLogics

    # def getEqps(self) -> Dict[str, MPLEqp]:
    #     try:
    #         if self.__eqpsGetState == RecvState.init:
    #             eqps = self.__eqpUseCase.getEqpList(FdcEqpReqDto(core=env('MP_CORE_ID')))
    #             for eqp in eqps:
    #                 self.__eqp[eqp.code] = MPLEqp(eqp)
    #             self.__eqpsGetState = RecvState.done
    #     except Exception as e:
    #         self.__logger.error(e.__str__())
    #         self.__logger.error(traceback.format_stack())
    #         traceback.print_stack()
    #         self.__eqpsGetState = RecvState.error
    #
    #     return self.__eqp

    def setMPLogicAPIRecvState(self, state: RecvState):
        self.__MPLogicRecvState = state
