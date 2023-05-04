from typing import Callable

from bFdcAPI.Eqp.UseCase import FdcEqpUseCase
from capa.Process.CapaEqp import CapaEqp
import json

class CapaListenerWorker:
    def __init__(self, capaEqps: dict[str, CapaEqp], workProcesses: list, capaPWorker: Callable) -> None:
        self.mpEqps = capaEqps
        self.workProcesses = workProcesses
        self.__fdcEqpUseCase = FdcEqpUseCase()
        self.__capaPWorker = capaPWorker

    def onMessage(self, message: str):
        r = json.loads(message)
        print(message)