import json
import logging
import traceback

from ACPContext.ACPContextImpl import ACPContextImpl
from FDCContext.logicConverter import decoratorLogicCode
from bFdcAPI.ACP.UseCase import ACPUseCase
from bFdcAPI.Enum import CommandModule, CommandAction


class ACPWorker:
    def __init__(self) -> None:
        super().__init__()
        self.acp_code = ACPUseCase.getACPLogicCode()
        if not self.acp_code.logicCode:
            return
        self.com = compile(decoratorLogicCode(self.acp_code.logicCode), '<string>', mode='exec')
        self.loggerAcp = logging.getLogger('acp')

    def messageParser(self, message: str):
        if not self.acp_code.logicCode:
            return
        try:
            exec(self.com, None, locals())
            context = ACPContextImpl()
            context.set_message(message)
            context.setLogger(self.loggerAcp)
            locals().get("run")(context)
        except Exception as e:
            self.loggerAcp.error(traceback.format_exc())
            self.loggerAcp.error(e.__str__())
            self.loggerAcp.error(traceback.format_stack())
            traceback.print_stack()

    def commandParser(self, message: str):
        loads = json.loads(message)
        if loads["Module"] == CommandModule.acpModule.value \
            and loads["Action"] == CommandAction.update.value \
                and loads["ModuleType"] == "logicCode":
            self.acp_code = ACPUseCase.getACPLogicCode()
            self.com = compile(decoratorLogicCode(self.acp_code.logicCode), '<string>', mode='exec')

