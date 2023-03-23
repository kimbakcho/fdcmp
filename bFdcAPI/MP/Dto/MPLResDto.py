from dataclasses import dataclass


@dataclass
class MPLResDto:
    id: int
    name: str
    logicCode: str
    returnType: str
    isBasic: bool
    orderIdx: int
    updateTime: str
    testMessage: str
