from dataclasses import dataclass
from typing import Optional


@dataclass
class FdcEqpReqDto:
    core: Optional[int]


@dataclass
class FdcEqpResDto:
    id: int
    code: str
    name: str
    updateTime: str
    process: int
    core: int
    orderIdx: int
