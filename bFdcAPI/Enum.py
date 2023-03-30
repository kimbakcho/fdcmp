from enum import Enum


class RecvState(Enum):
    init = 0
    done = 1
    error = 2


class EventType(Enum):
    start = "start"
    normal = "normal"
    end = "end"


class CommandModule(Enum):
    mcp = "mcp"
    mpl = "mpl"


class CommandType(Enum):
    event = "event"
    trace = "event"
    eventlv = "eventlv"
    traceGroup = "traceGroup"
    tracelv = "tracelv"
    conditions = "conditions"


class CommandAction(Enum):
    create = "create"
    update = "update"
    orderSwap = "orderSwap"
    delete = "delete"
