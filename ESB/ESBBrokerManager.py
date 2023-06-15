from enum import Enum
from typing import Optional

from ESB.ESBBroker import ESBBroker, ESBActiveMqBroker, ESBACPActiveMqBroker
from bFdcAPI.ACP.Dto.ACPMessageCoreSetting import ACPMessageCoreSettingResDto
from bFdcAPI.MP.Dto.Core import CoreResDto


class ESBBrokerType(Enum):
    ActiveMQ = "ActiveMQ"


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
        self.__acpBroker = None

    def getBroker(self, core: CoreResDto) -> Optional[ESBBroker]:
        if core.id in self.__connects.keys():
            return self.__connects[core.id]

        if core.brokerType == ESBBrokerType.ActiveMQ.value:
            self.__connects[core.id] = ESBActiveMqBroker(coreInfo=core)
            return self.__connects[core.id]
        return None

    def getACPBroker(self, setting: ACPMessageCoreSettingResDto) -> Optional[ESBBroker]:
        if self.__acpBroker:
            return self.__acpBroker
        else:
            if setting.brokerType == ESBBrokerType.ActiveMQ.value:
                self.__acpBroker = ESBACPActiveMqBroker(acpSetting=setting)
                return self.__acpBroker
