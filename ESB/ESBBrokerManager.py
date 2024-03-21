from enum import Enum
from typing import Optional

from ESB.ESBBroker import ESBBroker, ESBActiveMqBroker
from bFdcAPI.MP.Dto.Core import CoreResDto


class ESBBrokerType(Enum):
    ActiveMQ = "ActiveMQ"


class ESBBrokerManager:
    _instance = None

    # Singleton
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
            class_._instance.__connects = dict()
        return class_._instance


    def getBroker(self, core: CoreResDto) -> Optional[ESBBroker]:
        if core.id in self.__connects.keys():
            return self.__connects[core.id]

        if core.brokerType == ESBBrokerType.ActiveMQ.value:
            self.__connects[core.id] = ESBActiveMqBroker(coreInfo=core)
            return self.__connects[core.id]
        return None


