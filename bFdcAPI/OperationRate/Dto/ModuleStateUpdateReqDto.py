from dataclasses import dataclass




@dataclass
class ModuleStateUpdateReqDto:
    eqpModule: int
    state: str | None
    subState: str | None
    startTime: str
    comment: str
    force: bool
    etcInfo: dict | list
    isHuman: bool
    userName: bool | None
    fromSite: str
    mode: str | None