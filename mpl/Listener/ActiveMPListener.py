import traceback
from typing import Callable

from stomp import ConnectionListener
import logging

from bFdcAPI.Enum import CommandModule
from bFdcAPI.MP.Dto.Core import CoreResDto
from mpl.Process.MPEqp import MPEqp
from mpl.Process.MPLParserUtil import MPLParserUtil
from FDCContext.context import Context
import json

from mpl.Process.MPListenerWorker import MPListenerWorker


class ActiveMPListener(ConnectionListener):

    def __init__(self, coreInfo: CoreResDto, mpListenerWorker: MPListenerWorker) -> None:
        self.__core = coreInfo
        self.__logger = logging.getLogger('mpl')
        self.__mpListenerWorker = mpListenerWorker
    def on_connecting(self, host_and_port):
        self.__logger.debug(f"MPListener on_connecting = {host_and_port}")
        pass

    def on_connected(self, frame):
        self.__logger.debug(f"MPListener on_connected = {frame}")
        pass

    def on_disconnecting(self):
        self.__logger.debug("MPListener on_disconnecting")
        pass

    def on_disconnected(self):
        self.__logger.debug("MPListener on_disconnected")
        pass

    def on_heartbeat_timeout(self):
        self.__logger.debug("MPListener on_heartbeat_timeout")
        pass

    def on_before_message(self, frame):
        self.__logger.debug("MPListener on_before_message")
        pass

    def on_message(self, frame):
        try:
            if frame.headers['destination'] == self.__core.subject:
                self.__mpListenerWorker.onMessage(frame.body)
            elif frame.headers['destination'] == self.__core.commandSubject:
                self.__mpListenerWorker.onCommandMessage(frame.body)
        except Exception as e:
            self.__logger.error(e.__str__())
            self.__logger.error(traceback.format_stack())
            traceback.print_stack()

    def on_receipt(self, frame):
        self.__logger.debug("MPListener on_receipt")
        pass

    def on_error(self, frame):
        self.__logger.error(f"MPListener on_error = {frame}")
        pass

    def on_send(self, frame):
        pass

    def on_heartbeat(self):
        self.__logger.debug("MPListener on_heartbeat")
        pass

    def on_receiver_loop_completed(self, frame):
        self.__logger.debug("MPListener on_receiver_loop_completed")
        pass
