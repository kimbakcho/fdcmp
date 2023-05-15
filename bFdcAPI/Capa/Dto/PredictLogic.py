from dataclasses import dataclass


@dataclass
class PredictLogicResDto:
    id: int
    eqpModule: int
    trainLogic: int
    predictParams: dict
    testPredictParams: dict
    logic: str
    updateDate: str