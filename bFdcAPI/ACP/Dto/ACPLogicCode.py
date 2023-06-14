from dataclasses import dataclass


@dataclass
class ACPLogicCodeResDto:
    id: int
    testMessage: dict
    logicCode: str
    updateTime: str
    user: int