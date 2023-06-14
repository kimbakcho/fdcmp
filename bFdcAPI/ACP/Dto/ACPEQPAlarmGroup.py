from dataclasses import dataclass


@dataclass
class ACPEQPAlarmGroupResDto:
    id: int
    eqp: int
    alarmGroup: int
    orderIdx: int
    user: int
    alarmGroupName: str