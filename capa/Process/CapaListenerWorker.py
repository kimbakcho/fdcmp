import time
from multiprocessing import Process
from typing import Callable

from bFdcAPI.Enum import CommandModule, CommandAction, EqpModuleType
from bFdcAPI.Eqp.UseCase import FdcEqpUseCase
from capa.Process.CapaEqp import CapaEqp
import json

from capa.Process.CapaEqpModule import CapaEqpModule


class CapaListenerWorker:
    def __init__(self, capaEqps: dict[str, CapaEqp], workProcesses: list, capaPWorker: Callable) -> None:
        self.capaEqps = capaEqps
        self.workProcesses = workProcesses
        self.__fdcEqpUseCase = FdcEqpUseCase()
        self.__capaPWorker = capaPWorker

    def onMessage(self, message: str):
        r = json.loads(message)
        if r.get("Module") == CommandModule.eqpModule.value:
            if r.get("Action") in [CommandAction.update.value, CommandAction.delete.value]:
                if r.get("ModuleType") != EqpModuleType.capa.value:
                    self.deleteEqpModule(r.get("Eqp"), r.get("EqpCode"), r.get("EqpModule"))
                if r.get("ModuleType") == EqpModuleType.capa.value:
                    self.createEqpModule(r.get("Eqp"), r.get("EqpCode"), r.get("EqpModule"))
            elif r.get("Action") == CommandAction.create.value:
                self.createEqpModule(r.get("Eqp"), r.get("EqpCode"), r.get("EqpModule"))
        elif r.get("Module") == CommandModule.eqp.value:
            if r.get("Action") == CommandAction.delete.value:
                self.deleteEqp(r.get("Eqp"), r.get("EqpCode"))
            if r.get("Action") == CommandAction.update.value:
                self.updateEqp(r.get("Eqp"), r.get("EqpCode"))

    def updateEqp(self, eqpId: int, eqpCode: str):
        # if EqpCode Update
        if eqpCode not in self.capaEqps.keys():
            for mpEqp in self.capaEqps.values():
                if mpEqp.id == eqpId:
                    self.capaEqps.pop(mpEqp.code)
                    self.capaEqps[eqpCode] = mpEqp
                    mpEqp.code = eqpCode

    def deleteEqp(self, eqpId: int, eqpCode: str):
        if eqpCode in self.capaEqps.keys():
            self.capaEqps.pop(eqpCode)
            for process in self.workProcesses:
                if process["eqpId"] == eqpId:
                    self.workProcesses.remove(process)
                    process["process"].terminate()
                    time.sleep(0.1)
                    if process["process"].is_alive():
                        process["process"].kill()

    def createEqpModule(self, eqpId: int, eqpCode: str, eqpModuleId: int):
        if eqpCode not in self.capaEqps.keys():
            eqp = FdcEqpUseCase.getEqp(eqpId)
            self.capaEqps[eqpCode] = CapaEqp(eqp)
        capaEqp = self.capaEqps.get(eqpCode)
        if capaEqp.getModule(eqpModuleId) is None:
            res = FdcEqpUseCase.getEqpModule(eqpModuleId)
            if res.moduleType == EqpModuleType.capa.value:
                capaEqpModule = CapaEqpModule(res)
                capaEqp.addModule(capaEqpModule)
                capaProcess = Process(target=self.__capaPWorker,
                                  args=[capaEqpModule.id, capaEqpModule.messageQueue ],
                                  name=f'{capaEqp.name}_{capaEqpModule.name}',
                                  daemon=True)

                self.workProcesses.append(
                    {"process": capaProcess, "eqp": f'{capaEqp.name}', "eqpId": capaEqp.id, "moduleId": capaEqpModule.id,
                     "module": f'{capaEqpModule.name}'})

                capaProcess.start()

    def deleteEqpModule(self, eqpId: int, eqpCode: str, eqpModuleId: int):
        if eqpCode in self.capaEqps.keys():
            if self.capaEqps.get(eqpCode).getModule(eqpModuleId) is not None:
                self.capaEqps.get(eqpCode).removeModule(eqpModuleId)
                if self.capaEqps.get(eqpCode).getModules().__len__() == 0:
                    self.capaEqps.pop(eqpCode)
                for (index, process) in enumerate(self.workProcesses):
                    if (process["eqpId"] == eqpId) and (process["moduleId"] == eqpModuleId):
                        stopItem = self.workProcesses.pop(index)
                        stopItem["process"].terminate()
                        time.sleep(0.1)
                        if stopItem["process"].is_alive():
                            stopItem["process"].kill()
