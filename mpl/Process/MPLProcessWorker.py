import multiprocessing
import os
import threading
import traceback
from multiprocessing import Queue, Process, current_process
from pathlib import Path

from django.utils.log import configure_logging
from environ import environ
import time

from ESB.BrokerConnect import BrokerConnect, messageBrokerConnectManage
from ESB.ESBBrokerManager import ESBBrokerType
from bFdcAPI.Eqp.Dto.FdcEqp import FdcEqpReqDto
from bFdcAPI.Eqp.UseCase import FdcEqpUseCase
from bFdcAPI.MP.UseCase import FdcMpUseCase
from fdcmp.ProcessLogger import setLogger
from fdcmp.settings import BASE_DIR
from mpl.BrokerConnect.ActiveMqMPLConnect import ActiveMqMPLConnect
from mpl.Process.MPLWorker import MPLWorker
from mpl.Process.MPEqp import MPEqp
from django.apps import apps
from django.conf import settings
import logging
import re

from mpl.Process.MPLListenerWorker import MPLListenerWorker

env = environ.Env()

workProcesses = list()

mpUseCase = FdcMpUseCase()

mpEqps: dict[str, MPEqp] = dict()


def mplPWorker(moduleId: int, q: Queue, c: Queue):
    module = FdcEqpUseCase.getEqpModule(moduleId)
    eqpName = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", module.eqpName)
    eqpModuleName = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", module.name)
    logDir = f'{BASE_DIR}/log/mpl/{eqpName}/{eqpModuleName}/'
    Path(logDir).mkdir(parents=True, exist_ok=True)

    setLogger("mpl", f'{logDir}mplLog.log')
    setLogger("mcp", f'{logDir}mcpLog.log')
    loggerMpl = logging.getLogger('mpl')
    process = multiprocessing.current_process()
    loggerMpl.info(f"start mpl process({process.pid}) eqpName = {module.eqpName} moduleId={module.name}")
    if not apps.apps_ready:
        # configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)
        apps.populate(['mcp'])
    try:
        mplWorker = MPLWorker(moduleId, q, c)
        while True:
            try:
                if not q.empty():
                    try:
                        message = q.get()
                        loggerMpl.debug("mplPWorker Message")
                        loggerMpl.debug(message)
                        mplWorker.messageParser(message)
                    except Exception as e:
                        loggerMpl.error(e.__str__())
                        loggerMpl.error(traceback.print_stack())

                while not c.empty():
                    command = c.get()
                    mplWorker.commandParser(command)
                    loggerMpl.info(f'command[{current_process().name}]={command}')
                if q.empty():
                    time.sleep(0.1)
            except Exception as e:
                loggerMpl.error(traceback.format_exc())
                loggerMpl.error(e.__str__())
                loggerMpl.error(traceback.format_stack())
                traceback.print_stack()
    except Exception as e:
        loggerMpl.error(traceback.format_exc())
        loggerMpl.error(e.__str__())
        loggerMpl.error(traceback.format_stack())
        traceback.print_stack()


def mplProcessWorker():
    while True:
        try:
            fdcMpUseCase = FdcMpUseCase()
            eqps = FdcEqpUseCase.getEqpList(FdcEqpReqDto(core=env('MP_CORE_ID', int)))

            for eqp in eqps:
                mpEqps[eqp.code] = MPEqp(eqp)

            coreInfo = fdcMpUseCase.getCore(env('MP_CORE_ID', int))

            mplListenerWorker = MPLListenerWorker(mpEqps, workProcesses, mplPWorker)

            connect = None
            if coreInfo.brokerType == ESBBrokerType.ActiveMQ.value:
                connect = ActiveMqMPLConnect(mplListenerWorker, coreInfo)
            threading.Thread(target=messageBrokerConnectManage,
                             args=[connect, logging.getLogger("brokerMPLMessage")]).start()


            for mpEqp in mpEqps.values():
                for module in mpEqp.getModules():
                    process = Process(target=mplPWorker, args=[module.id, module.messageQueue, module.commandQueue],
                                      name=f'{mpEqp.name}_{module.name}', daemon=True)
                    workProcesses.append({"process": process, "eqp": f'{mpEqp.name}',
                                          "eqpId": mpEqp.id, "moduleId": module.id,
                                          "module": f'{module.name}'})
                    process.start()


            if connect is not None:
                connect.connect()
            return
        except Exception as e:
            logger = logging.getLogger("mpl")
            logger.error(traceback.format_exc())
            logger.error(e.__str__())
            logger.error(traceback.format_stack())
            traceback.print_stack()
            while workProcesses.__len__() > 0:
                process = workProcesses.pop()
                process.kill()
                process.kill.close()
            time.sleep(10)

