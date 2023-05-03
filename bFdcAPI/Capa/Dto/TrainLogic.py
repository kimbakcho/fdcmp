from dataclasses import dataclass


@dataclass
class TrainLogicResDto:
    id: int
    eqpModule: int
    logic: str
    model: str
    trainedModel: dict
    modelType: str
    updateDate: str