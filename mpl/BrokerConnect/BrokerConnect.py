import logging
import threading
import time
import traceback

import stomp

from bFdcAPI.MP.Dto.Core import CoreResDto
from mpl.Listener.MPLActiveListener import MPLActiveListener
from mpl.Process.MPLListenerWorker import MPLListenerWorker

from bFdcAPI import env


class BrokerConnect:

    def __init__(self, mplListenerWork: MPLListenerWorker) -> None:
        super().__init__()
        self._mplListenerWork = mplListenerWork

    def connect(self):
        pass

    def isConnect(self):
        pass


class ActiveMqConnect(BrokerConnect):

    def __init__(self, mplListenerWork: MPLListenerWorker, coreInfo: CoreResDto) -> None:
        super().__init__(mplListenerWork)
        self.__coreInfo = coreInfo


    def connect(self):
        try:
            self._c = stomp.Connection([(self.__coreInfo.ESBIp, self.__coreInfo.ESBPort)], reconnect_attempts_max=-1,
                                       reconnect_sleep_max=10.0)

            self._c.set_listener("mp", MPLActiveListener(self.__coreInfo, self._mplListenerWork))

            self._c.connect()

            self._c.subscribe(self.__coreInfo.subject, env('MP_CORE_ID') + "_message")

            self._c.subscribe(self.__coreInfo.commandSubject, env('MP_CORE_ID') + "_command")
        except Exception as e:
            logging.getLogger("mpl").error(e.__str__())
            logging.getLogger("mpl").error(traceback.format_stack())
            traceback.print_stack()

    def isConnect(self):
        return self._c.is_connected()
