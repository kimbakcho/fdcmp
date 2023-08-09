from dataclasses import dataclass


@dataclass
class ModuleStatePredictFinishTimeUpdateReqDto:
    eqpModule: int
    predictFinishTime: str