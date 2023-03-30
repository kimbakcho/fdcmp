import traceback

from stomp import ConnectionListener
import logging

from bFdcAPI.MP.Dto.Core import CoreResDto
from mpl.Process.MPEqp import MPEqp
from mpl.Process.MPLParserUtil import MPLParserUtil
from FDCContext.context import Context
import json



class MPListener(ConnectionListener):

    def __init__(self, coreInfo: CoreResDto,
                 mpEqps: dict[str, MPEqp]) -> None:
        super().__init__()
        self.__core = coreInfo
        self.mpEqps = mpEqps
        self.__mplUtil = MPLParserUtil()
        self.__logger = logging.getLogger('mpl')

    def on_connecting(self, host_and_port):
        self.__logger.info(f"MPListener on_connecting = {host_and_port}")
        pass

    def on_connected(self, frame):
        self.__logger.info(f"MPListener on_connected = {frame}")
        pass

    def on_disconnecting(self):
        self.__logger.info("MPListener on_disconnecting")
        pass

    def on_disconnected(self):
        self.__logger.info("MPListener on_disconnected")
        pass

    def on_heartbeat_timeout(self):
        pass

    def on_before_message(self, frame):
        pass

    def on_message(self, frame):
        try:
            if frame.headers['destination'] == self.__core.subject:
                context = Context()
                context.set_message(frame.body)
                for logicItem in self.__mplUtil.getMpLogics():
                    exec(logicItem.logicComPile, None, locals())
                    runResult = locals().get("run")(context)
                    context.mp[logicItem.name] = runResult
                    if logicItem.name == "EqpCode":
                        for module in self.mpEqps.get(context.mp[logicItem.name]).getModule():
                            module.messageQueue.put(frame.body)
                        break
            elif frame.headers['destination'] == self.__core.commandSubject:
                r = json.loads(frame.body)
                for module in self.mpEqps.get(r["EqpCode"]).getModule():
                    if "EqpModule" in r.keys():
                        if module.id == r["EqpModule"]:
                            module.commandQueue.put(frame.body)
        except Exception as e:
            self.__logger.error(e.__str__())
            self.__logger.error(traceback.format_stack())
            traceback.print_stack()

    def on_receipt(self, frame):
        pass

    def on_error(self, frame):
        self.__logger.error(f"MPListener on_error = {frame}")
        pass

    def on_send(self, frame):
        pass

    def on_heartbeat(self):
        pass

    def on_receiver_loop_completed(self, frame):
        pass
