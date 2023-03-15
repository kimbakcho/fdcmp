import environ

from bFdcEqp.Dto.FdcEqpLogicReqDto import FdcEqpLogicReqDto
from bFdcEqp.Dto.FdcEqpResDto import FdcEqpResDto
from bFdcEqp.views import FdcEqpUseCase
from FDCContext.context import Context

env = environ.Env()


class EqpInit:
    def __init__(self, eqp: FdcEqpResDto) -> None:
        self.eqpId = eqp.id
        self.fdcEqpUseCase = FdcEqpUseCase()
        initLogicRes = self.fdcEqpUseCase.getEqpLogicList(FdcEqpLogicReqDto(eqpId=eqp.id, name="init"))
        self.context = Context()
        for initItem in initLogicRes:
            self.com = compile(initItem.logicCode, '<string>', mode='exec')
            exec(self.com, None, locals())
            runResult = locals().get("run")(self.context)
