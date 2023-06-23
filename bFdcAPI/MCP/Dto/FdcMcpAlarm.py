from dataclasses import dataclass

from bFdcAPI.Enum import EventType


@dataclass
class FdcMcpAlarmResDto:
    id: int
    name: str
    alarmCode: str
    eqp: int
    eqpModule: int
    updateTime: str
    orderIdx: int
    testMessage: str
