from dataclasses import dataclass


@dataclass
class CycleTimeUpdateReqDto:
    eqpModule: int
    recipe: None | str
    type: None | str
    isSystem: bool
    cycleTime: float | int
    typeInfo: None | dict
    conditionInfo: None | dict


@dataclass
class CycleTimeReqDto:
    eqpCode: str
    recipe: str | None
    type: str | None


@dataclass
class CycleTimeManagerResDto:
    id: int
    type: str | None
    recipe: str | None
    cycleTime: float | int
    typeInfo: dict | None
    conditionInfo: dict | None
    eqpModule: int
    updateDate: str | None
    systemUpdate: bool | None
    user: str
