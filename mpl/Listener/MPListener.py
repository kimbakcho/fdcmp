
from stomp import ConnectionListener
import logging


from mpl.Process.MPLProcessWorker import mplMessageQueue

logger = logging.getLogger('mpl')


class MPListener(ConnectionListener):

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
        mplMessageQueue.put(frame)

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
