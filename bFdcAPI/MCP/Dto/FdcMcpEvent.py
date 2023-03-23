from dataclasses import dataclass


@dataclass
class FdcMcpEventResDto:
    id: int
    name: str
    eventCode: str
    eqp: int
    eqpModule: int
    updateTime: str
    orderIdx: int
