from stomp import ConnectionListener
import logging

from bFdcAPI.MP.Dto.Core import CoreResDto
from mpl.Process.MPEqp import MPEqp
from mpl.Process.MPLParserUtil import MPLParserUtil
from FDCContext.context import Context
import json
logger = logging.getLogger('mpl')


class MPListener(ConnectionListener):

    def __init__(self, coreInfo: CoreResDto,
                 mpEqps: dict[str, MPEqp]) -> None:
        super().__init__()
        self.__core = coreInfo
        self.__mpEqps = mpEqps
        self.__mplUtil = MPLParserUtil()

    def on_connecting(self, host_and_port):
        logger.info(f"on_connecting = {host_and_port}")
        pass

    def on_connected(self, frame):
        logger.info(f"on_connected = {frame}")
        pass

    def on_disconnecting(self):
        logger.info("on_disconnecting")
        pass

    def on_disconnected(self):
        logger.info("on_disconnected")
        pass

    def on_heartbeat_timeout(self):
        pass

    def on_before_message(self, frame):
        pass

    def on_message(self, frame):
        if frame.headers['destination'] == self.__core.subject:
            context = Context()
            context.set_message(frame.body)
            for logicItem in self.__mplUtil.getMpLogics():
                exec(logicItem.logicComPile, None, locals())
                runResult = locals().get("run")(context)
                context.mp[logicItem.name] = runResult
                if logicItem.name == "EqpCode":
                    for module in self.__mpEqps.get(context.mp[logicItem.name]).getModule():
                        module.messageQueue.put(frame.body)
                    break
        elif frame.headers['destination'] == self.__core.commandSubject:
            r = json.loads(frame.body)
            for module in self.__mpEqps.get(r["EqpCode"]).getModule():
                module.commandQueue.put(frame.body)

    def on_receipt(self, frame):
        pass

    def on_error(self, frame):
        logger.error(f"on_error = {frame}")
        pass

    def on_send(self, frame):
        logger.error(f"on_send = {frame}")
        pass

    def on_heartbeat(self):
        pass

    def on_receiver_loop_completed(self, frame):
        logger.error(f"on_receiver_loop_completed = {frame}")
        pass
