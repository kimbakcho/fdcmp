from multiprocessing import Queue

from bFdcAPI.Eqp.Dto.FdcEqpModule import FdcEqpModuleResDto


class MPEqpModule:

    def __init__(self, moduleResDto: FdcEqpModuleResDto) -> None:
        self.id = moduleResDto.id
        self.name = moduleResDto.name
        self.messageQueue = Queue()
        self.commandQueue = Queue()
