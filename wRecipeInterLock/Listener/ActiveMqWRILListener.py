import logging
import traceback

from stomp import ConnectionListener

from ESB.ListenerWorker import ListenerWorker
from wRecipeInterLock.bFdcAPI.Dto.RecipeInterLockSetting import RecipeInterLockSettingResDto


class ActiveMqWRILListener(ConnectionListener):
    def __init__(self, wrilSetting: RecipeInterLockSettingResDto, wrilListenerWorker: ListenerWorker) -> None:
        self.__logger = logging.getLogger('brokerWRILMessage')
        self.__wrilSetting = wrilSetting
        self.__wrilListenerWorker = wrilListenerWorker

    def on_connecting(self, host_and_port):
        self.__logger.info(f"ActiveMPListener on_connecting = {host_and_port}")
        pass

    def on_connected(self, frame):
        self.__logger.info(f"ActiveMPListener on_connected = {frame}")
        pass

    def on_disconnecting(self):
        self.__logger.info("ActiveMPListener on_disconnecting")
        pass

    def on_disconnected(self):
        self.__logger.info("ActiveMPListener on_disconnected")
        pass

    def on_heartbeat_timeout(self):
        self.__logger.info("ActiveMPListener on_heartbeat_timeout")
        pass

    def on_before_message(self, frame):
        self.__logger.info("ActiveMPListener on_before_message")
        pass

    def on_message(self, frame):
        try:
            self.__logger.info(frame.body)
            if frame.headers['destination'] == self.__wrilSetting.subject:
                self.__wrilListenerWorker.onMessage(frame.body)
            elif frame.headers['destination'] == self.__wrilSetting.commandSubject:
                self.__wrilListenerWorker.onCommandMessage(frame.body)
        except Exception as e:
            self.__logger.error("frame.body start")
            self.__logger.error(frame.body)
            self.__logger.error("frame.body end")
            self.__logger.error(traceback.format_exc())
            self.__logger.error(e.__str__())
            self.__logger.error(traceback.format_stack())
            traceback.print_stack()

    def on_receipt(self, frame):
        self.__logger.info("ActiveMPListener on_receipt")
        pass

    def on_error(self, frame):
        self.__logger.info(f"ActiveMPListener on_error = {frame}")
        pass

    def on_send(self, frame):
        pass

    def on_heartbeat(self):
        self.__logger.info("ActiveMPListener on_heartbeat")
        pass

    def on_receiver_loop_completed(self, frame):
        self.__logger.info("ActiveMPListener on_receiver_loop_completed")
        pass