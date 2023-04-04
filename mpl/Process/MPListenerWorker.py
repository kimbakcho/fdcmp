from typing import Callable

from bFdcAPI.Enum import CommandModule, CommandAction
from bFdcAPI.Eqp.UseCase import FdcEqpUseCase
from mpl.Process.MPEqp import MPEqp
from mpl.Process.MPEqpModule import MPEqpModule
from mpl.Process.MPLParserUtil import MPLParserUtil
from FDCContext.context import Context
import json
from multiprocessing import Process
import time


class MPListenerWorker:
    def __init__(self, mpEqps: dict[str, MPEqp], workProcesses: list, mplPWorker: Callable) -> None:
        self.mpEqps = mpEqps
        self.workProcesses = workProcesses
        self.__mplUtil = MPLParserUtil()
        self.__fdcEqpUseCase = FdcEqpUseCase()
        self.__mplPWorker = mplPWorker

    def onMessage(self, message: str):
        context = Context()
        context.set_message(message)
        for logicItem in self.__mplUtil.getMpLogics():
            exec(logicItem.logicComPile, None, locals())
            runResult = locals().get("run")(context)
            context.mp[logicItem.name] = runResult
            if logicItem.name == "EqpCode":
                if context.mp[logicItem.name] in self.mpEqps.keys():
                    for module in self.mpEqps.get(context.mp[logicItem.name]).getModules():
                        module.messageQueue.put(message)
                break

    def onCommandMessage(self, message: str):
        r = json.loads(message)
        if r.get("Module") == CommandModule.mpl.value:
            for eqp in self.mpEqps.values():
                for module in eqp.getModules():
                    module.commandQueue.put(message)
        elif r.get("Module") == CommandModule.mcp.value:
            if r["EqpCode"] in self.mpEqps.keys():
                for module in self.mpEqps.get(r["EqpCode"]).getModules():
                    if "EqpModule" in r.keys():
                        if module.id == r["EqpModule"]:
                            module.commandQueue.put(message)
        elif r.get("Module") == CommandModule.eqpModule.value:
            if r.get("Action") == CommandAction.create.value:
                self.createEqpModule(r.get("Eqp"), r.get("EqpCode"), r.get("EqpModule"))
            elif r.get("Action") == CommandAction.delete.value:
                self.deleteEqpModule(r.get("Eqp"), r.get("EqpCode"), r.get("EqpModule"))
        elif r.get("Module") == CommandModule.eqp.value:
            if r.get("Action") == CommandAction.delete.value:
                self.deleteEqp(r.get("Eqp"), r.get("EqpCode"))

    def deleteEqp(self, eqpId: int, eqpCode: str):
        if eqpCode in self.mpEqps.keys():
            self.mpEqps.pop(eqpCode)
            for process in self.workProcesses:
                if process["eqpId"] == eqpId:
                    self.workProcesses.remove(process)
                    process["process"].terminate()
                    time.sleep(0.1)
                    if process["process"].is_alive():
                        process["process"].kill()

    def createEqpModule(self, eqpId: int, eqpCode: str, eqpModuleId: int):
        if eqpCode not in self.mpEqps.keys():
            eqp = self.__fdcEqpUseCase.getEqp(eqpId)
            self.mpEqps.setdefault(eqpCode, MPEqp(eqp))
        mpEqp = self.mpEqps.get(eqpCode)
        if mpEqp.getModule(eqpModuleId) is None:
            res = self.__fdcEqpUseCase.getEqpModule(eqpModuleId)
            mpEqpModule = MPEqpModule(res)
            mpEqp.addModule(mpEqpModule)
            process = Process(target=self.__mplPWorker,
                              args=[mpEqpModule.id, mpEqpModule.messageQueue, mpEqpModule.commandQueue],
                              name=f'{mpEqp.name}_{mpEqpModule.name}',
                              daemon=True)
            self.workProcesses.append(
                {"process": process, "eqp": f'{mpEqp.name}', "eqpId": mpEqp.id, "moduleId": mpEqpModule.id,
                 "module": f'{mpEqpModule.name}'})
            process.start()

    def deleteEqpModule(self, eqpId: int, eqpCode: str, eqpModuleId: int):
        if eqpCode in self.mpEqps.keys():
            if self.mpEqps.get(eqpCode).getModule(eqpModuleId) is not None:
                self.mpEqps.get(eqpCode).removeModule(eqpModuleId)
                if self.mpEqps.get(eqpCode).getModules().__len__() == 0:
                    self.mpEqps.pop(eqpCode)
                for (index, process) in enumerate(self.workProcesses):
                    if (process["eqpId"] == eqpId) and (process["moduleId"] == eqpModuleId):
                        stopItem = self.workProcesses.pop(index)
                        stopItem["process"].terminate()
                        time.sleep(0.1)
                        if stopItem["process"].is_alive():
                            stopItem["process"].kill()