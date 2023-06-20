import time
import traceback


class BrokerConnect:
    def connect(self):
        pass

    def isConnect(self):
        pass


def messageBrokerConnectManage(broker: BrokerConnect, logger):
    time.sleep(30)
    while (True):
        try:
            if not broker.isConnect():
                broker.connect()
                time.sleep(10)
            else:
                time.sleep(30)
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error(e.__str__())
            logger.error(traceback.format_stack())
            traceback.print_stack()
        time.sleep(10)
