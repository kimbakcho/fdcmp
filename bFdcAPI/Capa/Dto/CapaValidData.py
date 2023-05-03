from dataclasses import dataclass


@dataclass
class CapaValidDataResDto:
    id: int
    eqpModule: int
    logicCode: str
    trainData: dict | str
    validData: dict | str
    updateDate: str
