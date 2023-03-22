from dataclasses import dataclass


@dataclass
class ConditionsResDto:
    id: int
    name: str
    eqpModule: int
    logicCode: str
    isSave: bool
    isBasic: bool
    testMessage: str
    orderIdx: int
    returnType: str
    updateTime: str