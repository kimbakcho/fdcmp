from dataclasses import dataclass


@dataclass
class TraceLVResDto:
    id: int
    name: str
    traceGroup: int
    orderIdx: int
    logicCode: str
    returnType: str
    testMessage: str
    isSave: bool
    updateTime: str
