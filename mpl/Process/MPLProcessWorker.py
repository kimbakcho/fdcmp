import sys
import traceback
from multiprocessing import Queue, Process, current_process

import stomp
from django.utils.log import configure_logging
from environ import environ
import time

from ESB.ESBBrokerManager import ESBBrokerType
from bFdcAPI.Eqp.Dto.FdcEqp import FdcEqpReqDto
from bFdcAPI.Eqp.UseCase import FdcEqpUseCase
from bFdcAPI.MP.UseCase import FdcMpUseCase
from fdcmp.settings import BASE_DIR
from mpl.BrokerConnect.BrokerConnect import ActiveMqConnect
from mpl.Listener.ActiveMPListener import ActiveMPListener
from mpl.Process.MPLWorker import MPLWorker
from mpl.Process.MPEqp import MPEqp
from django.apps import apps
from django.conf import settings
import logging

from mpl.Process.MPListenerWorker import MPListenerWorker

env = environ.Env()

workProcesses = list()

mpUseCase = FdcMpUseCase()

mpEqps: dict[str, MPEqp] = dict()


# def setLogger(loggerName: str):
#     import logging
#     logger = logging.getLogger(loggerName)
#     logger.setLevel(logging.INFO)
#     formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s')
#     filehandler = logging.FileHandler(f'{BASE_DIR}/mpl/mplLog.log')
#     filehandler.setFormatter(formatter)
#     consoleHandler = logging.StreamHandler()
#     logger.addHandler(filehandler)
#     logger.addHandler(consoleHandler)


def mplPWorker(moduleId: int, q: Queue, c: Queue):
    loggerMpl = logging.getLogger('mpl')
    if not apps.apps_ready:
        configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)
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
                loggerMpl.error(e.__str__())
                loggerMpl.error(traceback.format_stack())
                traceback.print_stack()
    except Exception as e:
        loggerMpl.error(e.__str__())
        loggerMpl.error(traceback.format_stack())
        traceback.print_stack()


def mplProcessWorker():
    while True:
        try:
            fdcMpUseCase = FdcMpUseCase()

            fdcEqpUseCase = FdcEqpUseCase()

            eqps = fdcEqpUseCase.getEqpList(FdcEqpReqDto(core=env('MP_CORE_ID', int)))

            for eqp in eqps:
                mpEqps.setdefault(eqp.code, MPEqp(eqp))

            coreInfo = fdcMpUseCase.getCore(env('MP_CORE_ID', int))

            mpListenerWorker = MPListenerWorker(mpEqps, workProcesses, mplPWorker)

            connect = None
            if coreInfo.brokerType == ESBBrokerType.ActiveMQ.value:
                connect = ActiveMqConnect(mpListenerWorker, coreInfo)

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
            # logger = logging.getLogger("mpl")
            # logger.error(e.__str__())
            # logger.error(traceback.format_stack())
            # traceback.print_stack()
            time.sleep(10)
