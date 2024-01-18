from dataclasses import dataclass


@dataclass
class PerformanceOperationRateSaveReqDto:
    eqpModule: int
    startTime: str
    endTime: str
    predictCycleTime: int | float
    initStartTime: str | None
    dueSec: int | None
    lotId: list | None
    batchId: str | None
    recipe: str | None
    type: str | None
    typeInfo: dict | None
    contextInfo: dict | None
    waferCount: int | None
    batchCount: int | None
    cycleTime: int | float | None
    realCycleTime: int | float | None
    productionCycleTime: int | float | None

