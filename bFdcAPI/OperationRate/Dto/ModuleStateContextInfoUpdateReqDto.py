from dataclasses import dataclass


@dataclass
class ModuleStateContextInfoUpdateReqDto:
    eqpModule: int
    info: dict | list | None
