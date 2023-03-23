from dataclasses import dataclass


@dataclass
class MBLResDto:
    id: int
    sourceIp: str
    sourcePort: int
    subject: str
    commandSubject: str
    updateTime: str
    brokerType: str