from enum import Enum

from pymongo import MongoClient

class TrainValidDataContext:
    def debug(self, msg: str):
        pass

    def setTrainData(self, value: dict):
        pass

    def getTrainData(self) -> dict:
        pass

    def setValidData(self, value: dict):
        pass

    def getValidData(self) -> dict:
        pass

    def setLogger(self, logger):
        pass

    def logMessage(self, message: str):
        pass

    def getMCPDBConnect(self) -> MongoClient:
        pass


class TrainLogicModel:
    def __init__(self, model, name, type) -> None:
        self.model = model
        self.name = name
        self.type = type


class TrainLogicContext:
    def debug(self, msg: str) -> None:
        pass

    def getTrainData(self) -> dict | None:
        pass

    def getValidData(self) -> dict | None:
        pass

    def setTrainModel(self, model: TrainLogicModel) -> None:
        pass

    def getTrainModels(self) -> dict[str, TrainLogicModel] | None:
        pass


class PredictParamInfoContext:
    def __init__(self, eqpModule: int) -> None:
        pass

    def debug(self, msg: str) -> None:
        pass

    def getTrainData(self) -> dict | None:
        pass

    def getValidData(self) -> dict | None:
        pass

    def setPredictParamInfo(self, params: dict) -> None:
        pass

    def getPredictParamInfo(self):
        pass

    def setPredictEtcInfo(self, params: dict) -> None:
        pass

    def getPredictEtcInfo(self) -> dict:
        pass

    def getMCPDBConnect(self) -> MongoClient:
        pass


class PredictLogicContext:
    def __init__(self, eqpModule: int) -> None:
        pass

    def debug(self, msg: str) -> None:
        pass

    def setPredictParams(self, params: dict) -> None:
        pass

    def getPredictParams(self) -> dict:
        pass

    def getPredictParamInfos(self) -> dict:
        pass

    def setPredictResult(self, predictResult: dict) -> None:
        pass

    def getPredictResult(self) -> dict:
        pass

    def getModel(self, name):
        pass
