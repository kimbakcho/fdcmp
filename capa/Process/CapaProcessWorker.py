import datetime
import logging
import time
import traceback
from multiprocessing import Queue, Process

from django.utils.log import configure_logging
from environ import environ

from ESB.ESBBrokerManager import ESBBrokerType
from bFdcAPI.Capa.Dto.TrainSchedulerHistory import TrainSchedulerHistoryListReqDto
from bFdcAPI.Capa.UseCase import CapaUseCase
from bFdcAPI.Enum import EqpModuleType
from bFdcAPI.Eqp.Dto.FdcEqp import FdcEqpReqDto
from bFdcAPI.Eqp.UseCase import FdcEqpUseCase
from bFdcAPI.MP.UseCase import FdcMpUseCase
from django.apps import apps
from capa.BrokerConnect.CapaBrokerConnect import CapaActiveMqConnect
from capa.Process.CapaEqp import CapaEqp
from capa.Process.CapaListenerWorker import CapaListenerWorker
from django.conf import settings

from capa.Process.CapaSchedulerWorker import CapaSchedulerWorker
from fdcmp.ProcessLogger import setLogger
from fdcmp.settings import BASE_DIR

env = environ.Env()

workProcesses = list()

capaEqps: dict[str, CapaEqp] = dict()

def capaPWorker(moduleId: int,q: Queue):
    setLogger("capa", f'{BASE_DIR}/capa/capaLog.log')
    logger = logging.getLogger("capa")
    logger.info(f"start process moduleId={moduleId}")
    while True:
        capaSchedulerWorker = CapaSchedulerWorker()
        try:
            capaSchedulerWorker.start()
        except Exception as e:
            logger = logging.getLogger("capa")
            logger.error(e.__str__())
            logger.error(traceback.format_stack())
            traceback.print_stack()
        time.sleep(1)

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
                    if module.moduleType == EqpModuleType.capa.value:
                        capaProcess = Process(target=capaPWorker, args=[module.id, module.messageQueue],
                                          name=f'{capaEqp.name}_{module.name}', daemon=True)
                        workProcesses.append({"process": capaProcess, "eqp": f'{capaEqp.name}',
                                              "eqpId": capaEqp.id, "moduleId": module.id,
                                              "module": f'{module.name}'})
                        capaProcess.start()

            if connect is not None:
                connect.connect()
            return
        except Exception as e:
            logger = logging.getLogger("capa")
            logger.error(e.__str__())
            logger.error(traceback.format_stack())
            traceback.print_stack()
            time.sleep(10)