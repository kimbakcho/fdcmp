from dataclasses import dataclass


@dataclass
class ACPAlarmGroupResDto:
    id: int
    groupName: str
    updateTime: str
    user: int
    groupInfo: dict
    orderIdx: int