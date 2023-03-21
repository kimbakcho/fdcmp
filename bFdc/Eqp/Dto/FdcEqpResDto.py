from dataclasses import dataclass


@dataclass
class FdcEqpResDto:
    id: int
    code: str
    name: str
    updateTime: str
    process: int
    core: int
    orderIdx: int
