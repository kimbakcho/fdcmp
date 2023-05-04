from multiprocessing import Queue

from bFdcAPI.Eqp.Dto.FdcEqpModule import FdcEqpModuleResDto


class CapaEqpModule:

    def __init__(self, moduleResDto: FdcEqpModuleResDto) -> None:
        self.id = moduleResDto.id
        self.name = moduleResDto.name
        self.messageQueue = Queue()
        self.moduleType = moduleResDto.moduleType

