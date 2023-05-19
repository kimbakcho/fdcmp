from dataclasses import dataclass


@dataclass
class TrainValidDataResDto:
    id: int
    eqpModule: int
    logicCode: str
    trainData: dict | str
    validData: dict | str
    trainPeriodStart: str| None
    trainPeriodEnd: str | None
    updateDate: str

@dataclass
class TrainValidDataUpdateReqDto:
    id: int
    trainData: dict | str
    validData: dict | str
    trainPeriodStart: str | None
    trainPeriodEnd: str | None