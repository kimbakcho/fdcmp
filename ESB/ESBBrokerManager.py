from enum import Enum

from ESB.ESBBroker import ESBBroker, ESBActiveMqBroker
from bFdcAPI.MP.Dto.Core import CoreResDto


class ESBBrokerType(Enum):
    ActiveMq = "ActiveMq"


class ESBBrokerManager:
    _instance = None

    # Singleton
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__(self) -> None:
        super().__init__()
        self.__connects = dict()

    def getBroker(self, core: CoreResDto) -> ESBBroker | None:
        if core.id in self.__connects.keys():
            return self.__connects[core.id]

        if core.brokerType == ESBBrokerType.ActiveMq.value:
            self.__connects[core.id] = ESBActiveMqBroker(coreInfo=core)
            return self.__connects[core.id]
        return None
