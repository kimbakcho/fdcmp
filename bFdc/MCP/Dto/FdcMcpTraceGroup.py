from dataclasses import dataclass


@dataclass
class FdcMcpTraceGroupResDto:
    id: int
    name: str
    eqpModule: int
    traceGroupCode: str
    updateTime: str
    orderIdx: int
