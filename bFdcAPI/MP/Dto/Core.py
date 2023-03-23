from dataclasses import dataclass


@dataclass
class CoreResDto:
    id: int
    ESBIp: str
    ESBPort: int
    subject: str
    commandSubject: str
    updateTime: str
    brokerType: str
