from dataclasses import dataclass


@dataclass
class TrainValidDataResDto:
    id: int
    eqpModule: int
    logicCode: str
    trainData: dict | str | None
    validData: dict | str | None
    trainPeriodStart: str | None
    trainPeriodEnd: str | None
    updateDate: str

    def __init__(self, id: int, eqpModule: int, logicCode: str,
                 updateDate: str,
                 trainData: dict | str | None = None,
                 validData: dict | str | None = None,
                 trainPeriodStart: str | None = None,
                 trainPeriodEnd: str | None = None
                 ) -> None:
        super().__init__()
        self.id = id
        self.eqpModule = eqpModule
        self.logicCode = logicCode
        self.updateDate = updateDate
        self.trainData = trainData
        self.validData = validData
        self.trainPeriodStart = trainPeriodStart
        self.trainPeriodEnd = trainPeriodEnd


@dataclass
class TrainValidDataUpdateReqDto:
    id: int
    trainData: dict | str
    validData: dict | str
    trainPeriodStart: str | None
    trainPeriodEnd: str | None
