from dataclasses import dataclass


@dataclass
class ModuleStateEtcInfoUpdateReqDto:
    eqpModule: int
    info: dict | list | None
