from bFdc.Eqp.Dto.FdcEqpReqDto import FdcEqpReqDto
from bFdc.Eqp.Dto.FdcEqpResDto import FdcEqpResDto
from bFdc.Eqp.UseCase import FdcEqpUseCase
from bFdc.MP.UseCase import FdcMpUseCase
from fdcmp.settings import env
from mpl.Process.MPLEqp import MPLEqp


class MPLParserUtil:
    def __init__(self) -> None:
        super().__init__()
        self.__mpLogics = []

        self.__eqp: dict[str, MPLEqp] = dict()
        self.mpUseCase = FdcMpUseCase()
        self.eqpUseCase = FdcEqpUseCase()

    def getMpLogics(self):
        if self.__mpLogics.__len__() == 0:

            for mpl in self.mpUseCase.getMPL():
                com = None
                if mpl.logicCode is not None:
                    com = compile(mpl.logicCode, '<string>', mode='exec')
                self.__mpLogics.append({"name": mpl.name, "compile": com})
        return self.__mpLogics

    def getEqps(self):
        if self.__eqp.__len__() == 0:
            eqps = self.eqpUseCase.getEqpList(FdcEqpReqDto(core=env('MP_CORE_ID')))
            for eqp in eqps:
                self.__eqp[eqp.code] = MPLEqp(eqp)
        return self.__eqp
