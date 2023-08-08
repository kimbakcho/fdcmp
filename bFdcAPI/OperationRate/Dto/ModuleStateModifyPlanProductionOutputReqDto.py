from dataclasses import dataclass


@dataclass
class ModuleStateModifyPlanProductionOutputReqDto:
    eqpModule: int
    count: int
