import logging
import threading
import time
import traceback

import stomp

from bFdcAPI.MP.Dto.Core import CoreResDto
from mpl.Listener.ActiveMPListener import ActiveMPListener
from mpl.Process.MPListenerWorker import MPListenerWorker

from bFdcAPI import env


class BrokerConnect:

    def __init__(self, mpListenerWork: MPListenerWorker) -> None:
        super().__init__()
        self._mpListenerWork = mpListenerWork

    def reConnect(self):
        pass

    def connect(self):
        pass

    def isConnect(self):
        pass


class ActiveMqConnect(BrokerConnect):

    def __init__(self, mpListenerWork: MPListenerWorker, coreInfo: CoreResDto) -> None:
        super().__init__(mpListenerWork)
        self.__coreInfo = coreInfo
        self._connectManagerStartFlag = False

    def reConnect(self):
        while self._connectManagerStartFlag:
            if not self.isConnect():
                try:
                    self._c.connect()
                    self._c.subscribe(self.__coreInfo.subject, env('MP_CORE_ID') + "_message")
                    self._c.subscribe(self.__coreInfo.commandSubject, env('MP_CORE_ID') + "_command")
                except Exception as e:
                    logging.getLogger("mpl").error(e.__str__())
                    logging.getLogger("mpl").error(traceback.format_stack())
            time.sleep(5)

    def connect(self):
        try:
            self._c = stomp.Connection([(self.__coreInfo.ESBIp, self.__coreInfo.ESBPort)])

            self._c.set_listener("mp", ActiveMPListener(self.__coreInfo, self._mpListenerWork))

            self._c.connect()

            self._c.subscribe(self.__coreInfo.subject, env('MP_CORE_ID') + "_message")

            self._c.subscribe(self.__coreInfo.commandSubject, env('MP_CORE_ID') + "_command")
        except Exception as e:
            logging.getLogger("mpl").error(e.__str__())
            logging.getLogger("mpl").error(traceback.format_stack())

        self._connectManagerStartFlag = True

        threading.Thread(target=self.reConnect).start()

    def isConnect(self):
        return self._c.is_connected()
