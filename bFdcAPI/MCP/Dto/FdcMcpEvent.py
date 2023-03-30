from dataclasses import dataclass

from bFdcAPI.Enum import EventType


@dataclass
class FdcMcpEventResDto:
    id: int
    name: str
    eventCode: str
    eqp: int
    eqpModule: int
    eventType: str
    updateTime: str
    orderIdx: int
