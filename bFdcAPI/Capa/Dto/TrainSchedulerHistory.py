from dataclasses import dataclass


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


@dataclass
class TrainSchedulerHistoryUpdateReqDto:
    id: int
    execute: bool | None
    executeTime: str | None
    predictResult: str | None
    trainedModel: str | None
    paramInfo: str | None
