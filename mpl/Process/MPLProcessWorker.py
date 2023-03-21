import json
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


def mplPWorker(q: Queue, c: Queue):
    import logging
    loggerMpl = logging.getLogger('mpl')
    loggerMpl.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s')
    handler = logging.FileHandler(f'{BASE_DIR}/mpl/mplLog.log')
    handler.setFormatter(formatter)
    loggerMpl.addHandler(handler)
    try:
        mpl_state = MPLParserUtil()
        mplWorker = MPLWorker(q, c, mpl_state)
        while True:
            try:
                if not q.empty():
                    try:
                        message = q.get()
                        mplWorker.context.set_message(message)
                        mplWorker.messageParser(message)
                    except Exception as e:
                        mplWorker.loggerMpl.error(e.__str__())
                        mplWorker.loggerMpl.error(traceback.print_stack())
                while not c.empty():
                    command = c.get()
                    mplWorker.context.set_message(command)
                    mplWorker.commandParser(command)
                    mplWorker.loggerMpl.info(f'command[{current_process().name}]={command}')
                else:
                    time.sleep(0.1)
            except Exception as e:
                loggerMpl.error(e.__str__())
                loggerMpl.error(traceback.print_stack())
    except Exception as e:
        loggerMpl.error(e.__str__())
        loggerMpl.error(traceback.print_stack())


def mplThWorker():
    commandMessageQueue.put(json.dumps({"command": SystemCommand.systemInit.value}))
    for p in range(env("MPL_WORKER", int)):
        process = Process(target=mplPWorker, args=(mplMessageQueue, commandMessageQueue),
                          daemon=True,
                          name=f'{p}')
        workProcesses.append({"process": process, "commandQueue": commandMessageQueue})
        process.start()
