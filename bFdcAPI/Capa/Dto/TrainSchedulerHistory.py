from dataclasses import dataclass, field
from typing import Optional

import dataclasses


@dataclass
class TrainSchedulerHistoryListReqDto:
    execute: bool | None
    trainScheduler__eqpModule: int
    planTime__lte: str | None


@dataclass
class TrainSchedulerHistoryResDto:
    id: int
    trainScheduler: int
    execute: bool
    executeTime: str | None
    planTime: str
    predictResult: list | dict | None
    trainedModel: dict | None
    paramInfo: dict | None



