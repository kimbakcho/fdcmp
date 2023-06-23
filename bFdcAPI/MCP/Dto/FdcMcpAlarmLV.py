from dataclasses import dataclass


@dataclass
class FdcMcpAlarmLVResDto:
    id: int
    name: str
    alarm: int
    logicCode: str
    returnType: str
    updateTime: str
    orderIdx: int
    isSave: bool
