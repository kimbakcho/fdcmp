import logging
import multiprocessing
import threading
import time
import traceback
from multiprocessing import Process, Queue

from ESB.BrokerConnect import messageBrokerConnectManage
from ESB.ESBBrokerManager import ESBBrokerType
from fdcmp.ProcessLogger import setLogger
from fdcmp.settings import BASE_DIR
from wRecipeInterLock.BorokerConnect.ActiveMqWRILConnect import ActiveMqWRILConnect
from wRecipeInterLock.Process.WRILListenerWorker import WRILListenerWorker
from wRecipeInterLock.Process.WRILWorker import WRILWorker
from wRecipeInterLock.bFdcAPI.UseCase import WRecipeInterLockUseCase

def wrilPWorker(q: Queue, c: Queue):
    logPath = f'{BASE_DIR}/log/wRecipeInterLock/wRILLog.log'
    setLogger("wRIL", logPath)
    loggerWRIL = logging.getLogger('wRIL')
    process = multiprocessing.current_process()
    loggerWRIL.info(f"WRILWorker PID = {process.pid}")
    try:
        wrilWorker = WRILWorker()
        while True:
            try:
                if not q.empty():
                    try:
                        message = q.get()
                        wrilWorker.messageParser(message)
                    except Exception as e:
                        loggerWRIL.error(e.__str__())
                        loggerWRIL.error(traceback.print_stack())
                    while not c.empty():
                        command = c.get()
                        wrilWorker.commandParser(command)
                if q.empty():
                    time.sleep(0.1)
            except Exception as e:
                loggerWRIL.error(traceback.format_exc())
                loggerWRIL.error(e.__str__())
                loggerWRIL.error(traceback.format_stack())
                traceback.print_stack()
    except Exception as e:
        loggerWRIL.error(traceback.format_exc())
        loggerWRIL.error(e.__str__())
        loggerWRIL.error(traceback.format_stack())
        traceback.print_stack()

def wrilProcessWorker():
    while True:
        try:
            wrilSetting = WRecipeInterLockUseCase.getSetting()
            wrilListenerWorker = WRILListenerWorker()
            connect = None
            if wrilSetting.brokerType == ESBBrokerType.ActiveMQ.value:
                connect = ActiveMqWRILConnect(wrilListenerWorker, wrilSetting)

            threading.Thread(target=messageBrokerConnectManage,
                             args=[connect, logging.getLogger("brokerWRILMessage")]).start()

            process = Process(target=wrilPWorker, args=[wrilListenerWorker.q, wrilListenerWorker.c],
                              name='wril', daemon=True)
            process.start()
            if connect is not None:
                connect.connect()
            return
        except Exception as e:
            logger = logging.getLogger("wRIL")
            logger.error(traceback.format_exc())
            logger.error(e.__str__())
            logger.error(traceback.format_stack())
            traceback.print_stack()
            time.sleep(10)
