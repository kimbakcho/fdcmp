from dataclasses import dataclass


@dataclass
class ACPMessageCoreSettingResDto:
    id: int
    sourceIp: str
    sourcePort: int
    subject: str
    commandSubject: str
    brokerType: str
    updateTime: str
