from dataclasses import dataclass


@dataclass
class ModuleStateDisplayInfoUpdateReqDto:
    eqpModule: int
    info: dict | list | None
