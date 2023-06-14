class ACPContext:
    def debug(self, msg: str):
        pass

    def setLogger(self, logger):
        pass

    def logMessage(self, message: str):
        pass

    def get_message(self) -> str:
        pass

    def set_message(self, value: str):
        pass

    def getEqpAlarmGroups(self, eqpCode: str) -> list[dict]:
        pass

    def getAlarmGroup(self, groupName: str) -> dict|None:
        pass

    def getEqpInfo(self, eqpCode: str) -> dict|None:
        pass