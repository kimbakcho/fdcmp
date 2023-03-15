import logging
import traceback
from multiprocessing import Queue, Process, current_process
from environ import environ
import time

from fdcmp.settings import BASE_DIR
from mpl.Process.MPLWorker import MPLWorker

mplMessageQueue = Queue()

env = environ.Env()

workProcesses = list()


def mplPWorker(q: Queue, c: Queue):
    import logging
    loggerMpl = logging.getLogger('mpl')
    loggerMpl.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s')
    handler = logging.FileHandler(f'{BASE_DIR}/mpl/mplLog.log')
    handler.setFormatter(formatter)
    loggerMpl.addHandler(handler)
    try:
        mplWorker = MPLWorker(q, c)
        while True:
            if not q.empty():
                try:
                    message = q.get()
                    mplWorker.context.set_message(message.body)
                    mplWorker.messageParser(message.body)
                    while not c.empty():
                        command = c.get()
                        mplWorker.context.set_message(command.body)
                        mplWorker.commandParser(command.body)
                        mplWorker.loggerMpl.info(f'command[{current_process().name}]={command}')
                except Exception as e:
                    mplWorker.loggerMpl.error(e.__str__())
                    mplWorker.loggerMpl.error(traceback.print_stack())
            else:
                time.sleep(0.1)
    except Exception as e:
        loggerMpl.error(e.__str__())
        loggerMpl.error(traceback.print_stack())


def mplThWorker():
    for p in range(env("MPL_WORKER", int)):
        commandMessageQueue = Queue()
        process = Process(target=mplPWorker, args=(mplMessageQueue, commandMessageQueue,), daemon=True)
        workProcesses.append({"process": process, "commandQueue": commandMessageQueue})
        process.start()
