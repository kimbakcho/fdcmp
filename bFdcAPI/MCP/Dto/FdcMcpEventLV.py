from dataclasses import dataclass


@dataclass
class FdcMcpEventLVResDto:
    id: int
    name: str
    event: int
    logicCode: str
    returnType: str
    updateTime: str
    orderIdx: int
    isSave: bool
