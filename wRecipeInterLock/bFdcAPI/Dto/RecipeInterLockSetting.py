from dataclasses import dataclass


@dataclass
class RecipeInterLockSettingResDto:
    id: int
    sourceIp: str
    sourcePort: int
    subject: str
    commandSubject: str
    updateTime: str
    brokerType: str