from dataclasses import dataclass, field
from typing import Optional


@dataclass
class FdcEqpModuleReqDto:
    eqp: Optional[int]


@dataclass
class FdcEqpModuleResDto:
    id: int
    code: str
    name: str
    eqpName: str
    eqp: int
    updateTime: str
    orderIdx: int
    moduleType: str
