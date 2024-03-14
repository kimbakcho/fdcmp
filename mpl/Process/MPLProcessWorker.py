import multiprocessing
import threading
import traceback
from multiprocessing import Queue, Process, current_process
from pathlib import Path

from django.apps import apps
from environ import environ
import time

from ESB.BrokerConnect import messageBrokerConnectManage
from ESB.ESBBrokerManager import ESBBrokerType
from bFdcAPI.Eqp.Dto.FdcEqp import FdcEqpReqDto
from bFdcAPI.Eqp.UseCase import FdcEqpUseCase
from bFdcAPI.MP.UseCase import FdcMpUseCase
from fdcmp.ProcessLogger import setLogger
from fdcmp.settings import BASE_DIR
from mpl.BrokerConnect.ActiveMqMPLConnect import ActiveMqMPLConnect
from mpl.Process.MPLWorker import MPLWorker
from mpl.Process.MPEqp import MPEqp
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
    try:
        if not apps.apps_ready:
            # configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)
            apps.populate(['mcp'])
    except Exception as e:
        loggerMpl.error(traceback.format_exc())
        loggerMpl.error(e.__str__())
        loggerMpl.error(traceback.format_stack())
        traceback.print_stack()
    try:
        loggerMpl.info(f"startInit 1")
        loopCount = 0
        while True:
            try:
                mplWorker = MPLWorker(moduleId, q, c)
                loggerMpl.info(f"startInit 2")
                FdcEqpUseCase.sendEqpModuleAliveSignal(module.id)
                break
            except Exception as e:
                loggerMpl.error(traceback.format_exc())
                loggerMpl.error(e.__str__())
                loggerMpl.error(traceback.format_stack())
                traceback.print_stack()
                time.sleep(1)

        while True:
            try:
                if module.isDebug:
                    loggerMpl.info("mplPWorker1")
                if not q.empty():
                    try:
                        message = q.get(timeout=10)
                        if module.isDebug:
                            loggerMpl.info("mplPWorker2")
                        mplWorker.messageParser(message)
                        if module.isDebug:
                            loggerMpl.info("mplPWorker3")
                    except Exception as e:
                        loggerMpl.error(e.__str__())
                        loggerMpl.error(traceback.print_stack())
                while not c.empty():
                    if module.isDebug:
                        loggerMpl.info("mplPWorker4")
                    command = c.get(timeout=10)
                    if module.isDebug:
                        loggerMpl.info("mplPWorker5")
                    mplWorker.commandParser(command)
                    if module.isDebug:
                        loggerMpl.info("mplPWorker6")
                    loggerMpl.info(f'command[{current_process().name}]={command}')
                if q.empty():
                    time.sleep(0.1)
                loopCount = loopCount + 1
                if loopCount > 600:
                    FdcEqpUseCase.sendEqpModuleAliveSignal(module.id)
                    loopCount = 0
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
    connect = None
    while True:
        try:
            fdcMpUseCase = FdcMpUseCase()
            eqps = FdcEqpUseCase.getEqpList(FdcEqpReqDto(core=env('MP_CORE_ID', int)))

            for eqp in eqps:
                mpEqps[eqp.code] = MPEqp(eqp)

            coreInfo = fdcMpUseCase.getCore(env('MP_CORE_ID', int))

            mplListenerWorker = MPLListenerWorker(mpEqps, workProcesses, mplPWorker)
            if connect is None:
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

