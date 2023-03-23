from dataclasses import dataclass


@dataclass
class FdcEqpLogicResDto:
    id: int
    eqpId: str
    name: str
    logicCode: str
    returnType: str
    isBasic: bool
    orderIdx: int
    updateTime: str
    testMessage: str
    eqpName: str


@dataclass
class FdcEqpLogicReqDto:
    eqpId: int
    name: str
