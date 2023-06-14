from dataclasses import asdict

from ACPContext.Context import ACPContext
from bFdcAPI.ACP.UseCase import ACPUseCase
from bFdcAPI.Eqp.UseCase import FdcEqpUseCase


class ACPContextImpl(ACPContext):
    def __init__(self) -> None:
        super().__init__()
        self.__message = None
        self.debugMsgs = []

    def debug(self, msg: str):
        self.debugMsgs.append(msg)

    def setLogger(self, logger):
        self.logger = logger

    def logMessage(self, message: str):
        self.logger.info(message)

    def get_message(self):
        return self.__message

    def set_message(self, value: str):
        self.__message = value

    def getEqpAlarmGroup(self, eqpCode: str):
        result = list()
        for item in ACPUseCase.getACPEQPAlarmGroups(eqpCode):
            result.append(asdict(item))
        return result

    def getAlarmGroup(self, groupName: str):
        return asdict(ACPUseCase.getACPAlarmGroup(groupName))

    def getEqpInfo(self, eqpCode: str):
        return asdict(FdcEqpUseCase.getEqpFromCode(eqpCode))
