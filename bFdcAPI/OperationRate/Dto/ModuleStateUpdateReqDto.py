from dataclasses import dataclass


@dataclass
class ModuleStateUpdateReqDto:
    module: int
    state: str
    startTime: str
    comment: str
    etcInfo: dict | list
    isHuman: bool
    userName: bool | None
    fromSite: str