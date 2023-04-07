from enum import Enum

from typing import Dict, Optional

from bson import ObjectId


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
    def __init__(self, message: Optional[str] = None) -> None:
        self.debugMsgs = []
        super().__init__()
        self.__message = message
        self.mp = {}
        self.event = {}
        self.trace = {}
        self.conditions = {}
        self.etc = {}
        self.currentFdcDataGroup: Optional[ObjectId] = None

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
