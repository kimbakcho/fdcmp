import sys
import traceback
from multiprocessing import Queue, Process, current_process, Pool, Lock

import stomp
from environ import environ
import time

from bFdcAPI.Eqp.Dto.FdcEqp import FdcEqpReqDto
from bFdcAPI.Eqp.Dto.FdcEqpModule import FdcEqpModuleReqDto
from bFdcAPI.Eqp.UseCase import FdcEqpUseCase
from bFdcAPI.MP.UseCase import FdcMpUseCase
from command.value import SystemCommand
from fdcmp.settings import BASE_DIR
from mpl.Listener.MPListener import MPListener
from mpl.Process.MPLWorker import MPLWorker, MPLParserUtil
from mpl.Process.MPEqp import MPEqp
import logging

env = environ.Env()

workProcesses = list()

mpUseCase = FdcMpUseCase()


def setLogger(loggerName: str):
    import logging
    logger = logging.getLogger(loggerName)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s')
    filehandler = logging.FileHandler(f'{BASE_DIR}/mpl/mplLog.log')
    filehandler.setFormatter(formatter)
    consoleHandler = logging.StreamHandler(sys.stdout)
    logger.addHandler(filehandler)
    logger.addHandler(consoleHandler)


def mplPWorker(moduleId: int, q: Queue, c: Queue):
    setLogger('mpl')
    setLogger('mcp')

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
                else:
                    time.sleep(0.1)
            except Exception as e:
                loggerMpl.error(e.__str__())
                loggerMpl.error(traceback.print_stack())
    except Exception as e:
        loggerMpl.error(e.__str__())
        loggerMpl.error(traceback.print_stack())


def mplProcessWorker():
    fdcMpUseCase = FdcMpUseCase()

    fdcEqpUseCase = FdcEqpUseCase()

    eqps = fdcEqpUseCase.getEqpList(FdcEqpReqDto(core=env('MP_CORE_ID', int)))

    mpEqps: dict[str, MPEqp] = dict()

    for eqp in eqps:
        mpEqps.setdefault(eqp.code, MPEqp(eqp))

    coreInfo = fdcMpUseCase.getCore(env('MP_CORE_ID', int))

    c = stomp.Connection([(coreInfo.ESBIp, coreInfo.ESBPort)])

    c.set_listener("mp", MPListener(coreInfo, mpEqps))

    c.connect()

    c.subscribe(coreInfo.subject, env('MP_CORE_ID') + "_message")

    c.subscribe(coreInfo.commandSubject, env('MP_CORE_ID') + "_command")

    for mpEqp in mpEqps.values():
        for module in mpEqp.getModule():
            process = Process(target=mplPWorker, args=[module.id, module.messageQueue, module.commandQueue],
                              daemon=True,
                              name=f'{mpEqp.name}_{module.name}')
            workProcesses.append({"process": process, "eqp": f'{mpEqp.name}', "module": f'{module.name}'})
            process.start()
