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
