import logging

from stomp import ConnectionListener

from multiprocessing import Queue

from mpl.Process.MPLProcessWorker import workProcesses

logger = logging.getLogger('mpl')


class MPLCommandListener(ConnectionListener):
    def on_connecting(self, host_and_port):
        logger.info(f"on_Mpl_Command_connecting = {host_and_port}")
        pass

    def on_connected(self, frame):
        logger.info(f"on_Mpl_Command_connected = {frame}")
        pass

    def on_disconnecting(self):
        logger.info("on_Mpl_Command_disconnecting")
        pass

    def on_disconnected(self):
        logger.info("on_Mpl_Command_disconnected")
        pass

    def on_heartbeat_timeout(self):
        pass

    def on_before_message(self, frame):
        pass

    def on_message(self, frame):
        for process in workProcesses:
            commandQueue: Queue = process.get("commandQueue")
            commandQueue.put(frame)

    def on_receipt(self, frame):
        pass

    def on_error(self, frame):
        logger.error(f"on_Mpl_Command_error = {frame}")
        pass

    def on_send(self, frame):
        logger.error(f"on_Mpl_Command_send = {frame}")
        pass

    def on_heartbeat(self):
        pass

    def on_receiver_loop_completed(self, frame):
        logger.error(f"on_Mpl_Command_receiver_loop_completed = {frame}")
        pass
