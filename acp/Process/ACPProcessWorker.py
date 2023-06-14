import logging
import threading
import time
import traceback
from multiprocessing import Queue, Process

from ESB.BrokerConnect import messageBrokerConnectManage
from ESB.ESBBrokerManager import ESBBrokerType
from acp.BrokerConnect.ActiveMqACPConnect import ActiveMqACPConnect
from acp.Process.ACPListenerWorker import ACPListenerWorker
from acp.Process.ACPWorker import ACPWorker
from bFdcAPI.ACP.UseCase import ACPUseCase
from fdcmp.ProcessLogger import setLogger
from fdcmp.settings import BASE_DIR
from django.apps import apps

def acpPWorker(q: Queue, c: Queue):
    logPath = f'{BASE_DIR}/acp/log/acpLog.log'
    setLogger("acp", logPath)
    loggerAcp = logging.getLogger('acp')
    try:
        acpWorker = ACPWorker()
        while True:
            try:
                if not q.empty():
                    try:
                        message = q.get()
                        acpWorker.messageParser(message)
                    except Exception as e:
                        loggerAcp.error(e.__str__())
                        loggerAcp.error(traceback.print_stack())
                while not c.empty():
                    command = c.get()
                    acpWorker.commandParser(command)
                if q.empty():
                    time.sleep(0.1)
            except Exception as e:
                loggerAcp.error(traceback.format_exc())
                loggerAcp.error(e.__str__())
                loggerAcp.error(traceback.format_stack())
                traceback.print_stack()
    except Exception as e:
        loggerAcp.error(traceback.format_exc())
        loggerAcp.error(e.__str__())
        loggerAcp.error(traceback.format_stack())
        traceback.print_stack()


def acpProcessWorker():
    while True:
        try:
            acpSetting = ACPUseCase.getACPMessageCoreSetting()

            acpListenerWorker = ACPListenerWorker()
            connect = None
            if acpSetting.brokerType == ESBBrokerType.ActiveMQ.value:
                connect = ActiveMqACPConnect(acpListenerWorker, acpSetting)

            threading.Thread(target=messageBrokerConnectManage,
                             args=[connect, logging.getLogger("brokerACPMessage")]).start()

            process = Process(target=acpPWorker, args=[acpListenerWorker.q, acpListenerWorker.c],
                          name='acp', daemon=True)
            process.start()
            if connect is not None:
                connect.connect()
            return
        except Exception as e:
            logger = logging.getLogger("acp")
            logger.error(traceback.format_exc())
            logger.error(e.__str__())
            logger.error(traceback.format_stack())
            traceback.print_stack()
            time.sleep(10)
