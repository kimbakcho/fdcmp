import logging
import traceback

import stomp

from ESB.BrokerConnect import BrokerConnect
from ESB.ListenerWorker import ListenerWorker
from wRecipeInterLock.Listener.ActiveMqWRILListener import ActiveMqWRILListener
from wRecipeInterLock.bFdcAPI.Dto.RecipeInterLockSetting import RecipeInterLockSettingResDto


class ActiveMqWRILConnect(BrokerConnect):

    def __init__(self, wrilListenerWork: ListenerWorker, wrilSetting: RecipeInterLockSettingResDto) -> None:
        self._wrilListenerWork = wrilListenerWork
        self.__wrilSetting = wrilSetting

    def connect(self):
        try:
            self._c = stomp.Connection([(self.__wrilSetting.sourceIp, self.__wrilSetting.sourcePort)], reconnect_attempts_max=-1,
                                       reconnect_sleep_max=10.0, auto_content_length=False)

            self._c.set_listener("wril", ActiveMqWRILListener(self.__wrilSetting, self._wrilListenerWork))

            self._c.connect(wait=True)

            self._c.subscribe(self.__wrilSetting.subject, "wril_message")

            self._c.subscribe(self.__wrilSetting.commandSubject,  "wril_command")

            self._c.disconnect()
        except Exception as e:
            logging.getLogger("brokerWRILMessage").error(traceback.format_exc())
            logging.getLogger("brokerWRILMessage").error(e.__str__())
            logging.getLogger("brokerWRILMessage").error(traceback.format_stack())
            traceback.print_stack()

    def isConnect(self):
        return self._c.is_connected()