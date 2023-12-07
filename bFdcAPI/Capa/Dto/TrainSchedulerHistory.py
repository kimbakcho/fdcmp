from dataclasses import dataclass, field
from typing import Optional

import dataclasses

@dataclass
class TrainSchedulerResDto:
    id: int
    eqpModule: int
    interval: int | None
    updateDate: str | None
    enabled: bool | None

@dataclass
class TrainSchedulerHistoryListReqDto:
    execute: bool | None
    trainScheduler__eqpModule: int | None
    planTime__lte: str | None


@dataclass
class TrainSchedulerHistoryResDto:
    id: int
    trainScheduler: TrainSchedulerResDto
    execute: bool
    executeTime: str | None
    planTime: str
    predictResult: list | dict | None
    trainedModel: dict | None
    paramInfo: dict | None

    def __init__(self,id: int,
                 trainScheduler: dict,
                 execute: bool,
                 executeTime: str|None,
                 planTime: str,
                 predictResult: list | dict | None,
                 trainedModel: dict | None,
                 paramInfo: dict | None
                 ) -> None:
        self.id = id
        self.trainScheduler = TrainSchedulerResDto(**trainScheduler)
        self.execute = execute
        self.executeTime = executeTime
        self.planTime = planTime
        self.predictResult = predictResult
        self.trainedModel = trainedModel
        self.paramInfo = paramInfo







