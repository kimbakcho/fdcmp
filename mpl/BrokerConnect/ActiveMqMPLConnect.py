import logging
import traceback

import stomp

from ESB import ListenerWorker
from ESB.BrokerConnect import BrokerConnect
from bFdcAPI.MP.Dto.Core import CoreResDto
from mpl.Listener.MPLActiveListener import MPLActiveListener

from bFdcAPI import env


class ActiveMqMPLConnect(BrokerConnect):

    def __init__(self, mplListenerWork: ListenerWorker, coreInfo: CoreResDto) -> None:
        self._mplListenerWork = mplListenerWork
        self.__coreInfo = coreInfo
        logging.getLogger("mpl").info("create ActiveMqMPLConnect")
        self._c = stomp.Connection([(self.__coreInfo.ESBIp, self.__coreInfo.ESBPort)], reconnect_attempts_max=-1,
                                   reconnect_sleep_max=10.0, auto_content_length=False)
    def connect(self):
        try:
            if not self._c.is_connected():
                self._c.set_listener("mp", MPLActiveListener(self.__coreInfo, self._mplListenerWork))

                self._c.connect(wait=True)

                self._c.subscribe(self.__coreInfo.subject, env('MP_CORE_ID') + "_message")

                self._c.subscribe(self.__coreInfo.commandSubject, env('MP_CORE_ID') + "_command")

        except Exception as e:
            logging.getLogger("brokerMPLMessage").error(traceback.format_exc())
            logging.getLogger("brokerMPLMessage").error(e.__str__())
            logging.getLogger("brokerMPLMessage").error(traceback.format_stack())
            traceback.print_stack()

    def isConnect(self):
        if self.__dict__.get("_c"):
            return self._c.is_connected()
        else:
            return False
