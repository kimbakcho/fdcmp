import logging
import traceback

import stomp

from bFdcAPI.MP.Dto.Core import CoreResDto
from capa.Process.CapaListenerWorker import CapaListenerWorker
from capa.Listener.CapaActiveMPListener import CapaActiveListener
from bFdcAPI import env

class CapaBrokerConnect:
    def __init__(self, capaListenerWork: CapaListenerWorker) -> None:
        super().__init__()
        self._capaListenerWork = capaListenerWork

    def connect(self):
        pass

    def isConnect(self):
        pass

class CapaActiveMqConnect(CapaBrokerConnect):
    def __init__(self, capaListenerWork: CapaListenerWorker, coreInfo: CoreResDto) -> None:
        super().__init__(capaListenerWork)
        self.__coreInfo = coreInfo

    def connect(self):
        try:
            self._c = stomp.Connection([(self.__coreInfo.ESBIp, self.__coreInfo.ESBPort)], reconnect_attempts_max=-1,
                                       reconnect_sleep_max=10.0)

            self._c.set_listener("mp", CapaActiveListener(self.__coreInfo, self._capaListenerWork))

            self._c.connect(wait=True)

            self._c.subscribe(self.__coreInfo.capaSubject, env('MP_CORE_ID') + "_capaMessage")

        except Exception as e:
            logging.getLogger("capa").error(traceback.format_exc())
            logging.getLogger("capa").error(e.__str__())
            logging.getLogger("capa").error(traceback.format_stack())
            traceback.print_stack()

    def isConnect(self):
        return self._c.is_connected()
