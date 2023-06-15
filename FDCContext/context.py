from enum import Enum

from typing import Dict, Optional

from bson import ObjectId

from ESB.ESBBrokerManager import ESBBrokerManager
from bFdcAPI.ACP.Dto.ACPMessageCoreSetting import ACPMessageCoreSettingResDto
from bFdcAPI.ACP.UseCase import ACPUseCase


class ConditionsBasic(Enum):
    IsRun = "IsRun"
    LotId = "LotId"
    Step = "Step"
    Slot = "Slot"
    Recipe = "Recipe"
    Product = "Product"


class MpBasic(Enum):
    EqpCode = "EqpCode"
    IsTrace = "IsTrace"
    IsEvent = "IsEvent"
    IsAlarm = "IsAlarm"
    TraceGroupCode = "TraceGroupCode"
    EventCode = "EventCode"


class Context:
    def __init__(self) -> None:
        self.debugMsgs = []
        super().__init__()
        self.__message = None
        self.mp = {}
        self.event = {}
        self.trace = {}
        self.conditions = {}
        self.etc = {}
        self.contextHistory = list()
        self.currentFdcDataGroup: Optional[ObjectId] = None
        self.__acpSetting = None

    def setLogger(self, logger):
        self.logger = logger

    def logMessage(self, message: str):
        self.logger.info(message)

    def get_simpleContext(self) -> Dict:
        return {"MP": self.mp, "conditions": self.conditions}

    def getTraceValue(self, traceGroup, traceName):
        if traceGroup in self.trace.keys() and traceName in self.trace[traceGroup].keys():
            return self.trace.get(traceGroup).get(traceName)
        else:
            return None

    def getEventValue(self, eventGroup, eventName):
        if eventGroup in self.event.keys() and eventName in self.event[eventGroup].keys():
            return self.event.get(eventGroup).get(eventName)
        else:
            return None

    def getConditionsValue(self, conditionsName):
        if conditionsName in self.conditions.keys():
            return self.conditions.get(conditionsName)
        else:
            return None

    def get_message(self):
        return self.__message

    def set_message(self, value: str):
        self.__message = value

    def debug(self, msg: str):
        self.debugMsgs.append(msg)

    def setAPCMessageCoreSetting(self, apcSetting: ACPMessageCoreSettingResDto):
        self.__acpSetting = apcSetting

    def sendACPMessage(self, msg: str):
        if not self.__acpSetting:
            return
        acpBroker = ESBBrokerManager().getACPBroker(self.__acpSetting)
        acpBroker.sendMessage(msg)
