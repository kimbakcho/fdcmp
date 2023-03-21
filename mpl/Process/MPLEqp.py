from bFdc.Eqp.Dto.FdcEqpResDto import FdcEqpResDto


class MPLEqp:
    def __init__(self, resDto: FdcEqpResDto) -> None:
        super().__init__()
        self.name = resDto.name
        self.code = resDto.code
        self.id = resDto.id
        self.resDto = resDto

    def getModule(self):
        pass
