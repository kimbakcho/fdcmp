from dataclasses import dataclass


@dataclass
class CycleTimeUpdateReqDto:
    eqpModule: int
    paramName: None | str
    type: None | str
    isSystem: bool
    weight: float | int
    modelWeight: float | int | None
    performanceWeight: float | int | None
    typeInfo: None | dict
    conditionInfo: None | dict


@dataclass
class CycleTimeReqDto:
    eqpModule__eqp__code: str
    paramName: str | None
    type: str | None


@dataclass
class CycleTimeManagerResDto:
    id: int
    type: str | None
    paramName: str | None
    performanceWeight: float | int | None
    performanceWeightSystemUpdate: bool | None
    performanceWeightUpdateDate: str | None
    weight: float | int
    modelWeight: float | int | None
    typeInfo: dict | None
    conditionInfo: dict | None
    eqpModule: int
    updateDate: str | None
    systemUpdate: bool | None
    modelUpdateDate: str | None
    user: str
    acceptDocument: int | None
