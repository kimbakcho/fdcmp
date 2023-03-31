from enum import Enum


class RecvState(Enum):
    init = 0
    done = 1
    error = 2
    needReload = 3


class EventType(Enum):
    start = "start"
    normal = "normal"
    end = "end"


class CommandModule(Enum):
    mcp = "mcp"
    mpl = "mpl"
    eqpModule = "eqpModule"


class CommandType(Enum):
    event = "event"
    trace = "event"
    eventlv = "eventlv"
    traceGroup = "traceGroup"
    tracelv = "tracelv"
    conditions = "conditions"
    mpLogic = "mpLogic"


class CommandAction(Enum):
    create = "create"
    update = "update"
    orderSwap = "orderSwap"
    delete = "delete"
