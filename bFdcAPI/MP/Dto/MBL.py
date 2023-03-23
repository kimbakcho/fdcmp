from dataclasses import dataclass


@dataclass
class MBLResDto:
    id: int
    sourceIp: str
    sourcePort: int
    subject: str
    updateTime: str
    brokerType: str