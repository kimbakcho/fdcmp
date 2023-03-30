from ESB.ESBBroker import ESBBroker, ESBActiveMqBroker
from ESB.Enum import ESBBrokerType
from bFdcAPI.MP.Dto.Core import CoreResDto


class ESBBrokerManager:

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
