import logging
import traceback

import stomp

from ESB.BrokerConnect import BrokerConnect
from ESB.ListenerWorker import ListenerWorker
from acp.Listener.ActiveMqACPListener import ActiveMqACPListener
from bFdcAPI.ACP.Dto.ACPMessageCoreSetting import ACPMessageCoreSettingResDto


class ActiveMqACPConnect(BrokerConnect):
    def __init__(self, acpListenerWork: ListenerWorker, acpSetting: ACPMessageCoreSettingResDto) -> None:
        self._acpListenerWork = acpListenerWork
        self.__acpSetting = acpSetting

    def connect(self):
        try:
            self._c = stomp.Connection([(self.__acpSetting.sourceIp, self.__acpSetting.sourcePort)], reconnect_attempts_max=-1,
                                       reconnect_sleep_max=10.0, auto_content_length=False)

            self._c.set_listener("acp", ActiveMqACPListener(self.__acpSetting, self._acpListenerWork))

            self._c.connect(wait=True)

            self._c.subscribe(self.__acpSetting.subject, "acp_message")

            self._c.subscribe(self.__acpSetting.commandSubject,  "acp_command")
        except Exception as e:
            logging.getLogger("brokerACPMessage").error(traceback.format_exc())
            logging.getLogger("brokerACPMessage").error(e.__str__())
            logging.getLogger("brokerACPMessage").error(traceback.format_stack())
            traceback.print_stack()

    def isConnect(self):
        return self._c.is_connected()

