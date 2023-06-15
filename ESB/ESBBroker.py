import stomp

from bFdcAPI.ACP.Dto.ACPMessageCoreSetting import ACPMessageCoreSettingResDto
from bFdcAPI.MP.Dto.Core import CoreResDto


class ESBBroker:
    def sendMessage(self, message: str):
        pass

    def sendCommandMessage(self, message: str):
        pass

    def sendCapaMessage(self, message: str):
        pass


class ESBActiveMqBroker(ESBBroker):

    def __init__(self, coreInfo: CoreResDto) -> None:
        super().__init__()
        self.__coreInfo = coreInfo
        self.__c = stomp.Connection([(coreInfo.ESBIp, coreInfo.ESBPort)])

    def sendMessage(self, message: str):
        if not self.__c.is_connected():
            self.__c.connect(wait=True)
        self.__c.send(self.__coreInfo.subject, message)

    def sendCommandMessage(self, message: str):
        if not self.__c.is_connected():
            self.__c.connect(wait=True)
        self.__c.send(self.__coreInfo.commandSubject, message)

    def sendCapaMessage(self, message: str):
        if not self.__c.is_connected():
            self.__c.connect(wait=True)
        self.__c.send(self.__coreInfo.capaSubject, message)


class ESBACPActiveMqBroker(ESBBroker):

    def __init__(self, acpSetting: ACPMessageCoreSettingResDto) -> None:
        super().__init__()
        self.__acpSetting = acpSetting
        self.__c = stomp.Connection([(acpSetting.sourceIp, acpSetting.sourcePort)])

    def sendMessage(self, message: str):
        if not self.__c.is_connected():
            self.__c.connect(wait=True)
        self.__c.send(self.__acpSetting.subject, message)


    def sendCommandMessage(self, message: str):
        if not self.__c.is_connected():
            self.__c.connect(wait=True)
        self.__c.send(self.__acpSetting.commandSubject, message)
