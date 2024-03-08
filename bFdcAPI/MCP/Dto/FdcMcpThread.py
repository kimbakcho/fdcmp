
from dataclasses import dataclass,fields


@dataclass(init=False)
class ThreadingLoopResDto:
    id: int
    name: str
    eqpModule: int
    logicCode: str
    orderIdx: int
    interval: float
    updateTime: str

    def __init__(self, **kwargs):
        names = set([f.name for f in fields(self)])
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)