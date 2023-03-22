from dataclasses import dataclass


@dataclass
class FdcEqpModuleReqDto:
    eqp: int


@dataclass
class FdcEqpModuleResDto:
    id: int
    code: str
    name: str
    eqpName: str
    eqp: int
    updateTime: str
    orderIdx: int
