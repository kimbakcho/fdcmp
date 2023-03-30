from enum import Enum


class RecvState(Enum):
    init = 0
    done = 1
    error = 2

class EventType(Enum):
    start = "start"
    normal = "normal"
    end = "end"