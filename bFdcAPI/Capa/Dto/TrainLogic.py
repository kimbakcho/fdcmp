from dataclasses import dataclass


@dataclass
class TrainLogicResDto:
    id: int
    eqpModule: int
    logic: str
    model: str
    trainedModel: dict
    modelType: str
    trainedInfo: dict
    updateDate: str


@dataclass
class TrainLogicUpdateReqDto:
    id: int
    trainedModel: dict | str
    trainedInfo: dict | str