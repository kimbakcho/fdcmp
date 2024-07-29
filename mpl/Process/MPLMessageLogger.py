from datetime import datetime
import logging
import time
import traceback
from multiprocessing import Queue, Process
from mcp.Process.MCPMongoService import MCPMongoService


class MPLMessageLogger:
    def __init__(self):
        super().__init__()
        self.messageQueue = Queue()
        self.process = Process(target=self.run, args=(self.messageQueue,),daemon=True)


    def startProcess(self):
        self.process.start()


    def run(self, queue: Queue):
        __mongoService = MCPMongoService()
        indexes = __mongoService.list_indexes("messageLog")
        index_exists = False
        for index in indexes:
            if index["name"] == "EqpCode_1_updateTime_1":
                index_exists = True
                break
        if not index_exists:
            try:
                __mongoService.create_index("messageLog", "EqpCode_1_updateTime_1",[("EqpCode", 1), ("updateTime", 1)])
            except Exception as e:
                __loggerMpl = logging.getLogger("mpl")
                __loggerMpl.error(traceback.format_exc())
                __loggerMpl.error(e.__str__())
                __loggerMpl.error(traceback.format_stack())
            try:
                __mongoService.create_index("messageLog", "updateTime_1", [("updateTime", 1)],
                                            expireAfterSeconds=2*24*60*60)
            except Exception as e:
                __loggerMpl = logging.getLogger("mpl")
                __loggerMpl.error(traceback.format_exc())
                __loggerMpl.error(e.__str__())
                __loggerMpl.error(traceback.format_stack())
        while True:
            try:
                while not queue.empty():
                    message = queue.get()
                    eqp_code = message.get("EqpCode")
                    msg = message.get("Message")
                    __mongoService.insert("messageLog",{
                        "EqpCode": eqp_code,
                        "Message": msg,
                        "updateTime": datetime.now(),
                    })
                time.sleep(0.1)
            except Exception as e:
                __loggerMpl = logging.getLogger("mpl")
                __loggerMpl.error(traceback.format_exc())
                __loggerMpl.error(e.__str__())
                __loggerMpl.error(traceback.format_stack())
                __mongoService.close()
                time.sleep(10)

