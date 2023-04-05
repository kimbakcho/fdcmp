from dataclasses import dataclass


@dataclass
class MLBResDto:
    id: int
    sourceIp: str
    sourcePort: int
    subject: str
    commandSubject: str
    updateTime: str
    brokerType: str