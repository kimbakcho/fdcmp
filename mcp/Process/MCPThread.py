import logging
import time
import traceback

from FDCContext.context import Context
from FDCContext.logicConverter import decoratorLogicCode
from bFdcAPI.MCP.Dto.FdcMcpThread import ThreadingLoopResDto
import threading


class MCPThread:
    def __init__(self, context: Context, threadingResDto: ThreadingLoopResDto) -> None:
        super().__init__()
        self.threadingResDto = threadingResDto
        self.com = compile(decoratorLogicCode(self.threadingResDto.logicCode), '<string>', mode='exec')
        self.context = context
        self.__logger = logging.getLogger('mcp')
        self.thread: None | threading.Thread = None
        self.stopEvents = threading.Event()

    def loopCode(self):
        while not self.stopEvents.is_set():
            try:
                exec(self.com, None, locals())
                locals().get("run")(self.context)
            except Exception as e:
                self.__logger.error(f'{self.context.getEqpName()}_{self.context.getModuleName()}_{self.thread.name}')
                self.__logger.error(traceback.format_exc())
                self.__logger.error(e.__str__())
                self.__logger.error(traceback.format_stack())
                traceback.print_stack()
            time.sleep(self.threadingResDto.interval)

    def startLoop(self):
        threadName = f"{self.context.getEqpName()}_{self.context.getModuleName()}_{self.threadingResDto.name}"
        self.thread = threading.Thread(target=self.loopCode, daemon=True, name=threadName)
        self.thread.start()

    def stop(self):
        if self.thread is not None:
            self.stopEvents.set()
