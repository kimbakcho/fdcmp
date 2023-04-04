

import stomp

from bFdcAPI.MP.Dto.Core import CoreResDto


class ESBBroker:
    def sendMessage(self, message: str):
        pass

    def sendCommandMessage(self, message: str):
        pass


class ESBActiveMqBroker(ESBBroker):

    def __init__(self, coreInfo: CoreResDto) -> None:
        super().__init__()
        self.__coreInfo = coreInfo
        self.__c = stomp.Connection([(coreInfo.ESBIp, coreInfo.ESBPort)])

    def sendMessage(self, message: str):
        if not self.__c.is_connected():
            self.__c.connect()
        self.__c.send(self.__coreInfo.subject, message)

    def sendCommandMessage(self, message: str):
        if not self.__c.is_connected():
            self.__c.connect()
        self.__c.send(self.__coreInfo.commandSubject, message)
