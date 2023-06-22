import logging
import multiprocessing
import time
import traceback
from multiprocessing import Queue, Process
from pathlib import Path

from environ import environ

from ESB.ESBBrokerManager import ESBBrokerType
from bFdcAPI.Enum import EqpModuleType
from bFdcAPI.Eqp.Dto.FdcEqp import FdcEqpReqDto
from bFdcAPI.Eqp.UseCase import FdcEqpUseCase
from bFdcAPI.MP.UseCase import FdcMpUseCase
from capa.BrokerConnect.CapaBrokerConnect import CapaActiveMqConnect
from capa.Process.CapaEqp import CapaEqp
from capa.Process.CapaListenerWorker import CapaListenerWorker
from capa.Process.CapaSchedulerWorker import CapaSchedulerWorker
from fdcmp.ProcessLogger import setLogger
from fdcmp.settings import BASE_DIR
import re

env = environ.Env()

capaWorkProcesses = list()

capaEqps: dict[str, CapaEqp] = dict()


def capaPWorker(moduleId: int, q: Queue):
    eqpModule = FdcEqpUseCase.getEqpModule(moduleId)
    eqpName = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", eqpModule.eqpName)
    eqpModuleName = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", eqpModule.eqpName)
    logDir = f'{BASE_DIR}/capa/log/{eqpName}/{eqpModuleName}/'

    Path(logDir).mkdir(parents=True, exist_ok=True)
    setLogger("capa", f'{logDir}capaLog.log')
    logger = logging.getLogger("capa")
    process = multiprocessing.current_process()
    logger.info(f"start capa process({process.pid}) moduleId={moduleId}")

    while True:
        capaSchedulerWorker = CapaSchedulerWorker(eqpModule)
        try:
            capaSchedulerWorker.start()
        except Exception as e:
            logging.getLogger("capa").error(f'{eqpModule.eqpName}_{eqpModule.name}')
            logger = logging.getLogger("capa")
            logger.error(traceback.format_exc())
            logger.error(e.__str__())
            logger.error(traceback.format_stack())
            traceback.print_stack()
        time.sleep(60)


def capaProcessWorker():
    while True:
        try:
            fdcMpUseCase = FdcMpUseCase()

            eqps = FdcEqpUseCase.getEqpList(FdcEqpReqDto(core=env('MP_CORE_ID', int)))

            for eqp in eqps:
                capaEqps[eqp.code] = CapaEqp(eqp)

            coreInfo = fdcMpUseCase.getCore(env('MP_CORE_ID', int))

            capaListenerWorker = CapaListenerWorker(capaEqps, capaWorkProcesses, capaPWorker)

            connect = None
            if coreInfo.brokerType == ESBBrokerType.ActiveMQ.value:
                connect = CapaActiveMqConnect(capaListenerWorker, coreInfo)

            for capaEqp in capaEqps.values():
                for module in capaEqp.getModules():
                    if module.moduleType == EqpModuleType.capa.value:
                        capaProcess = Process(target=capaPWorker, args=[module.id, module.messageQueue],
                                              name=f'{capaEqp.name}_{module.name}', daemon=True)
                        capaWorkProcesses.append({"process": capaProcess, "eqp": f'{capaEqp.name}',
                                              "eqpId": capaEqp.id, "moduleId": module.id,
                                              "module": f'{module.name}'})
                        capaProcess.start()

            if connect is not None:
                connect.connect()
            return
        except Exception as e:
            logger = logging.getLogger("capa")
            logger.error(traceback.format_exc())
            logger.error(e.__str__())
            logger.error(traceback.format_stack())
            traceback.print_stack()
            time.sleep(10)
            while capaWorkProcesses.__len__() > 0:
                process = capaWorkProcesses.pop()
                process.kill()
                process.kill.close()
            time.sleep(10)
