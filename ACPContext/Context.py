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

    def getEqpAlarmGroup(self, eqpCode: str) -> list[dict]:
        pass

    def getAlarmGroup(self, groupName: str) -> dict:
        pass

    def getEqpInfo(self, eqpCode: str) -> dict:
        pass