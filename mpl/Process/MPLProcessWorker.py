import json
import sys
import threading
import traceback
from multiprocessing import Queue, Process, current_process, Pool, Lock
from environ import environ
import time

from bFdc.MP.UseCase import FdcMpUseCase
from command.value import SystemCommand
from fdcmp.settings import BASE_DIR
from mpl.Process.MPLWorker import MPLWorker, MPLParserUtil

mplMessageQueue = Queue()

env = environ.Env()

workProcesses = list()

commandMessageQueue = Queue()

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


def mplPWorker(q: Queue, c: Queue):
    setLogger('mpl')
    setLogger('mcp')
    import logging
    loggerMpl = logging.getLogger('mpl')
    try:
        mplWorker = MPLWorker(q, c)
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
    commandMessageQueue.put(json.dumps({"command": SystemCommand.systemInit.value}))
    for p in range(env("MPL_WORKER", int)):
        process = Process(target=mplPWorker, args=(mplMessageQueue, commandMessageQueue),
                          daemon=True,
                          name=f'{p}')
        workProcesses.append({"process": process, "commandQueue": commandMessageQueue})
        process.start()
