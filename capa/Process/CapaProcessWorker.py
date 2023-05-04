import logging
import time
import traceback
from multiprocessing import Queue, Process

from environ import environ

from ESB.ESBBrokerManager import ESBBrokerType
from bFdcAPI.Eqp.Dto.FdcEqp import FdcEqpReqDto
from bFdcAPI.Eqp.UseCase import FdcEqpUseCase
from bFdcAPI.MP.UseCase import FdcMpUseCase
from capa.BrokerConnect.CapaBrokerConnect import CapaActiveMqConnect
from capa.Process.CapaEqp import CapaEqp
from capa.Process.CapaListenerWorker import CapaListenerWorker

env = environ.Env()

workProcesses = list()

capaEqps: dict[str, CapaEqp] = dict()

def capaPWorker(moduleId: int,q: Queue):
    pass

def capaProcessWorker():
    while True:
        try:
            fdcMpUseCase = FdcMpUseCase()

            fdcEqpUseCase = FdcEqpUseCase()

            eqps = fdcEqpUseCase.getEqpList(FdcEqpReqDto(core=env('MP_CORE_ID', int)))

            for eqp in eqps:
                capaEqps[eqp.code] = CapaEqp(eqp)

            coreInfo = fdcMpUseCase.getCore(env('MP_CORE_ID', int))

            capaListenerWorker = CapaListenerWorker(capaEqps,workProcesses,capaPWorker)

            connect = None
            if coreInfo.brokerType == ESBBrokerType.ActiveMQ.value:
                connect = CapaActiveMqConnect(capaListenerWorker, coreInfo)

            for capaEqp in capaEqps.values():
                for module in capaEqp.getModules():
                    if module.moduleType == "Capa":
                        process = Process(target=capaPWorker, args=[module.id, module.messageQueue],
                                          name=f'{capaEqp.name}_{module.name}', daemon=True)
                        workProcesses.append({"process": process, "eqp": f'{capaEqp.name}',
                                              "eqpId": capaEqp.id, "moduleId": module.id,
                                              "module": f'{module.name}'})
            if connect is not None:
                connect.connect()
            return
        except Exception as e:
            logger = logging.getLogger("capa")
            logger.error(e.__str__())
            logger.error(traceback.format_stack())
            traceback.print_stack()
            time.sleep(10)