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
