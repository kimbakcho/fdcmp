import datetime

import CapaContext.Context
from bFdcAPI import env
from pymongo import MongoClient
import base64
import json
import pickle

from bFdcAPI.Capa.Dto.CycleTime import CycleTimeUpdateReqDto
from bFdcAPI.Capa.UseCase import CapaUseCase


class MCPDBConnect:
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
            class_._instance._client = MongoClient(
                host=env("MCP_DB_HOST"),
                port=env("MCP_DB_PORT", int),
                username=env("MCP_DB_USER_NAME"),
                password=env("MCP_DB_PASS"),
                authSource=env("MCP_DB_AUTH_SOURCE"),
                authMechanism=env("MCP_DB_AUTH_MECHANISM"),
                tz_aware=True,
                connect=True
            )

        return class_._instance

    def getDBConnect(self):
        return self._client


class TrainValidDataContext(CapaContext.Context.TrainValidDataContext):

    def __init__(self) -> None:
        self.debugMsgs = []
        self._mcpDBConnect = MCPDBConnect()
        self.trainValidData = dict()
        self._trainValue = dict()
        self._validValue = dict()
        self._trainPeriodStart = None
        self._trainPeriodEnd = None
        self._eqpCode = None
        self._eqpName = None
        self._eqpModuleCode = None
        self._eqpModuleName = None

    def debug(self, msg: str):
        self.debugMsgs.append(msg)

    def setTrainData(self, value: dict):
        self._trainValue = value

    def getTrainData(self) -> dict:
        return self._trainValue

    def setValidData(self, value: dict):
        self._validValue = value

    def getValidData(self) -> dict:
        return self._validValue

    def setLogger(self, logger):
        self.logger = logger

    def logMessage(self, message: str):
        self.logger.info(message)

    def getMCPDBConnect(self) -> MongoClient:
        return self._mcpDBConnect.getDBConnect()

    def setTrainPeriodStart(self, value):
        self._trainPeriodStart = value

    def setTrainPeriodEnd(self, value):
        self._trainPeriodEnd = value

    def getTrainPeriodStart(self):
        return self._trainPeriodStart

    def getTrainPeriodEnd(self):
        return self._trainPeriodEnd

    def setEqpCode(self, value: str):
        self._eqpCode = value

    def getEqpCode(self):
        return self._eqpCode

    def setEqpName(self, value: str):
        self._eqpName = value

    def getEqpName(self):
        return self._eqpName

    def setEqpModuleCode(self, value: str):
        self._eqpModuleCode = value

    def getEqpModuleCode(self):
        return self._eqpModuleCode

    def setEqpModuleName(self, value: str):
        self._eqpModuleName = value

    def getEqpModuleName(self):
        return self._eqpModuleName


class TrainLogicContext(CapaContext.Context.TrainLogicContext):

    def __init__(self, eqpModule: int) -> None:
        self.debugMsgs = []
        self._predictParams = dict()
        self.trainValidData = dict()
        self._trainedInfo = dict()
        self._eqpModule = eqpModule
        self._model = dict()
        self._eqpCode = None
        self._eqpName = None
        self._eqpModuleCode = None
        self._eqpModuleName = None

    def debug(self, msg: str) -> None:
        self.debugMsgs.append(msg)

    def getTrainData(self) -> dict | None:
        res = CapaUseCase.getTrainValidData(self._eqpModule)
        return res.trainData

    def getValidData(self) -> dict | None:
        res = CapaUseCase.getTrainValidData(self._eqpModule)
        return res.validData

    def setTrainModel(self, model: CapaContext.Context.TrainLogicModel) -> None:
        self._model[model.name] = model

    def getTrainModels(self) -> dict[str, CapaContext.Context.TrainLogicModel] | None:
        return self._model

    def setTrainedInfo(self, value: dict) -> None:
        self._trainedInfo = value

    def getTrainedInfo(self) -> dict | None:
        return self._trainedInfo

    def setEqpCode(self, value: str):
        self._eqpCode = value

    def getEqpCode(self):
        return self._eqpCode

    def setEqpName(self, value: str):
        self._eqpName = value

    def getEqpName(self):
        return self._eqpName

    def setEqpModuleCode(self, value: str):
        self._eqpModuleCode = value

    def getEqpModuleCode(self):
        return self._eqpModuleCode

    def setEqpModuleName(self, value: str):
        self._eqpModuleName = value

    def getEqpModuleName(self):
        return self._eqpModuleName

    def updateCycleTime(self, recipe: str, cycleTime: float | int, type: str | None = None,
                        typeInfo: dict | None = None,
                        conditionInfo: dict | None = None):
        reqDto = CycleTimeUpdateReqDto(
            eqpModule=self._eqpModule,
            recipe=recipe,
            cycleTime=cycleTime,
            type=type,
            typeInfo=typeInfo,
            isSystem=True,
            conditionInfo=conditionInfo,
        )
        CapaUseCase.updateCycleTime(reqDto)


class PredictParamInfoContext(CapaContext.Context.PredictParamInfoContext):

    def __init__(self, eqpModule: int) -> None:
        self.debugMsgs = []
        self._mcpDBConnect = MCPDBConnect()
        self._paramInfo = dict()
        self._predictParamsInfo = dict()
        self._eqpModule = eqpModule
        self._etcInfo = dict()
        self._eqpCode = None
        self._eqpName = None
        self._eqpModuleCode = None
        self._eqpModuleName = None

    def debug(self, msg: str) -> None:
        self.debugMsgs.append(msg)

    def getTrainData(self) -> dict | None:
        res = CapaUseCase.getTrainValidData(self._eqpModule)
        return res.trainData

    def getValidData(self) -> dict | None:
        res = CapaUseCase.getTrainValidData(self._eqpModule)
        return res.validData

    def setPredictParamInfo(self, params: dict) -> None:
        self._paramInfo = params

    def getPredictParamInfo(self):
        return self._paramInfo

    def setPredictEtcInfo(self, params: dict) -> None:
        self._etcInfo = params

    def getPredictEtcInfo(self) -> dict:
        return self._etcInfo

    def getMCPDBConnect(self) -> MongoClient:
        return self._mcpDBConnect.getDBConnect()

    def setSchedulePredictParamInfo(self, params: dict | list) -> None:
        self._predictParamsInfo = params

    def getSchedulePredictParamInfo(self) -> dict | list:
        return self._predictParamsInfo

    def getTrainedInfo(self) -> dict | None:
        return CapaUseCase.getTrainLogic(self._eqpModule).trainedInfo

    def getTrainPeriodStart(self):
        res = CapaUseCase.getTrainValidData(self._eqpModule)
        return datetime.datetime.fromisoformat(res.trainPeriodStart)

    def getTrainPeriodEnd(self):
        res = CapaUseCase.getTrainValidData(self._eqpModule)
        return datetime.datetime.fromisoformat(res.trainPeriodEnd)

    def setEqpCode(self, value: str):
        self._eqpCode = value

    def getEqpCode(self):
        return self._eqpCode

    def setEqpName(self, value: str):
        self._eqpName = value

    def getEqpName(self):
        return self._eqpName

    def setEqpModuleCode(self, value: str):
        self._eqpModuleCode = value

    def getEqpModuleCode(self):
        return self._eqpModuleCode

    def setEqpModuleName(self, value: str):
        self._eqpModuleName = value

    def getEqpModuleName(self):
        return self._eqpModuleName


class PredictLogicContext(CapaContext.Context.PredictLogicContext):

    def __init__(self, eqpModule: int) -> None:
        self.debugMsgs = []
        self._predictParams = dict()
        self._eqpModule = eqpModule
        self._model = None
        self._predictResult = dict()
        self._eqpCode = None
        self._eqpName = None
        self._eqpModuleCode = None
        self._eqpModuleName = None

    def debug(self, msg: str) -> None:
        self.debugMsgs.append(msg)

    def setPredictParams(self, params: dict) -> None:
        self._predictParams = params

    def getPredictParams(self) -> dict:
        return self._predictParams

    def getPredictParamInfos(self) -> dict:
        return CapaUseCase.getPredictParamInfo(self._eqpModule).paramInfo

    def setPredictResult(self, predictResult: dict) -> None:
        self._predictResult = predictResult

    def getPredictResult(self) -> dict:
        return self._predictResult

    def getModel(self, name):
        trainedModels = CapaUseCase.getTrainLogic(self._eqpModule).trainedModel
        trainModelDict = trainedModels[name]
        if trainModelDict["type"] == "pickle":
            base64Model = trainModelDict["model"]
            model = base64.b64decode(base64Model)
            model = pickle.loads(model)
            return model
        raise Exception("can not deserialize")

    def setEqpCode(self, value: str):
        self._eqpCode = value

    def getEqpCode(self):
        return self._eqpCode

    def setEqpName(self, value: str):
        self._eqpName = value

    def getEqpName(self):
        return self._eqpName

    def setEqpModuleCode(self, value: str):
        self._eqpModuleCode = value

    def getEqpModuleCode(self):
        return self._eqpModuleCode

    def setEqpModuleName(self, value: str):
        self._eqpModuleName = value

    def getEqpModuleName(self):
        return self._eqpModuleName
