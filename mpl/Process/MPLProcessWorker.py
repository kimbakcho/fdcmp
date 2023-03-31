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
from mpl.Listener.MPListener import MPListener
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


def setLogger(loggerName: str):
    import logging
    logger = logging.getLogger(loggerName)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s')
    filehandler = logging.FileHandler(f'{BASE_DIR}/mpl/mplLog.log')
    filehandler.setFormatter(formatter)
    consoleHandler = logging.StreamHandler()
    logger.addHandler(filehandler)
    logger.addHandler(consoleHandler)


def mplPWorker(moduleId: int, q: Queue, c: Queue):
    configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)
    apps.populate(['mcp'])
    loggerMpl = logging.getLogger('mpl')
    try:
        mplWorker = MPLWorker(moduleId, q, c)
        while True:
            try:
                if not q.empty():
                    try:
                        message = q.get()
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
    fdcMpUseCase = FdcMpUseCase()

    fdcEqpUseCase = FdcEqpUseCase()

    eqps = fdcEqpUseCase.getEqpList(FdcEqpReqDto(core=env('MP_CORE_ID', int)))

    for eqp in eqps:
        mpEqps.setdefault(eqp.code, MPEqp(eqp))

    coreInfo = fdcMpUseCase.getCore(env('MP_CORE_ID', int))

    mpListenerWorker = MPListenerWorker(mpEqps, workProcesses, mplPWorker)

    if coreInfo.brokerType == ESBBrokerType.ActiveMq.value:
        c = stomp.Connection([(coreInfo.ESBIp, coreInfo.ESBPort)])

        c.set_listener("mp", MPListener(coreInfo, mpListenerWorker))

        c.connect()

        c.subscribe(coreInfo.subject, env('MP_CORE_ID') + "_message")

        c.subscribe(coreInfo.commandSubject, env('MP_CORE_ID') + "_command")

    for mpEqp in mpEqps.values():
        for module in mpEqp.getModules():
            process = Process(target=mplPWorker, args=[module.id, module.messageQueue, module.commandQueue],
                              name=f'{mpEqp.name}_{module.name}', daemon= True)
            workProcesses.append({"process": process, "eqp": f'{mpEqp.name}',
                                  "eqpId": mpEqp.id, "moduleId": module.id,
                                  "module": f'{module.name}'})
            process.start()
