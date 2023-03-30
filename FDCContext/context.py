from enum import Enum

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
    def __init__(self, message: str | None = None) -> None:
        self.debugMsgs = []
        super().__init__()
        self.__message = message
        self.mp = {}
        self.event = {}
        self.trace = {}
        self.conditions = {}
        self.currentFdcDataGroup: ObjectId | None = None

    def get_simpleContext(self) -> dict:
        return {"MP": self.mp, "event": self.event, "trace": self.trace, "conditions": self.conditions}

    def get_message(self):
        return self.__message

    def set_message(self, value: str):
        self.__message = value

    def debug(self, msg: str):
        self.debugMsgs.append(msg)