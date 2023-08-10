from dataclasses import dataclass, field, MISSING
from enum import Enum
from datetime import datetime
from typing import Dict, Optional

from bson import ObjectId

from ESB.ESBBrokerManager import ESBBrokerManager
from bFdcAPI.ACP.Dto.ACPMessageCoreSetting import ACPMessageCoreSettingResDto
from bFdcAPI.Capa.Dto.CycleTime import CycleTimeReqDto
from bFdcAPI.Capa.UseCase import CapaUseCase
from bFdcAPI.OperationRate.Dto.ModuleStateContextInfoUpdateReqDto import ModuleStateContextInfoUpdateReqDto
from bFdcAPI.OperationRate.Dto.ModuleStateDisplayInfoUpdateReqDto import ModuleStateDisplayInfoUpdateReqDto
from bFdcAPI.OperationRate.Dto.ModuleStateEtcInfoUpdateReqDto import ModuleStateEtcInfoUpdateReqDto
from bFdcAPI.OperationRate.Dto.ModuleStateModifyPlanProductionOutputReqDto import \
    ModuleStateModifyPlanProductionOutputReqDto
from bFdcAPI.OperationRate.Dto.ModuleStatePredictFinishTimeUpdateReqDto import ModuleStatePredictFinishTimeUpdateReqDto
from bFdcAPI.OperationRate.Dto.ModuleStateUpdateReqDto import ModuleStateUpdateReqDto
from bFdcAPI.OperationRate.Dto.PerformanceOperationRateSaveReqDto import PerformanceOperationRateSaveReqDto
from bFdcAPI.OperationRate.UseCase import OperationRateUseCase


class ConditionsBasic(Enum):
    IsRun = "IsRun"
    LotId = "LotId"
    Step = "Step"
    Slot = "Slot"
    Recipe = "Recipe"
    Product = "Product"


class MpBasic(Enum):
    EqpCode = "EqpCode"
    IsTrace = "IsTrace"
    IsEvent = "IsEvent"
    IsAlarm = "IsAlarm"
    TraceGroupCode = "TraceGroupCode"
    EventCode = "EventCode"
    AlarmCode = "AlarmCode"


@dataclass
class OperationStateReqDto:
    state: str | None
    startTime: datetime
    comment: str
    etcInfo: dict | list | None
    userName: str | None
    fromSite: str
    force: bool


class OperationAPIModule:
    Run = "Run"
    Wait = "Wait"

    def __init__(self, module: int) -> None:
        self.module = module

    def moduleStateUpdate(self, req: OperationStateReqDto):
        reqDto = ModuleStateUpdateReqDto(
            eqpModule=self.module,
            userName=req.userName,
            state=req.state,
            isHuman=False,
            startTime=req.startTime.isoformat(),
            fromSite=req.fromSite,
            etcInfo=req.etcInfo,
            comment=req.comment,
            force=req.force,
        )
        OperationRateUseCase.moduleStateUpdate(reqDto=reqDto)

    def moduleStateDisplayInfoUpdate(self, info: dict | list | None):
        reqDto = ModuleStateDisplayInfoUpdateReqDto(
            eqpModule=self.module,
            info=info
        )
        OperationRateUseCase.moduleStateDisplayInfoUpdate(reqDto=reqDto)

    def moduleStateContextInfoUpdate(self, info: dict | list | None):
        reqDto = ModuleStateContextInfoUpdateReqDto(
            eqpModule=self.module,
            info=info
        )
        OperationRateUseCase.moduleStateContextInfoUpdate(reqDto=reqDto)

    def moduleStateEtcInfoUpdate(self, info: dict | list | None):
        reqDto = ModuleStateEtcInfoUpdateReqDto(
            eqpModule=self.module,
            info=info
        )
        OperationRateUseCase.moduleStateEtcInfoUpdate(reqDto=reqDto)

    def moduleStateAddProductionOutput(self, count: int):
        reqDto = ModuleStateModifyPlanProductionOutputReqDto(
            eqpModule=self.module,
            count=count
        )
        OperationRateUseCase.moduleStateAddProductionOutput(reqDto)

    def performanceOperationRateHistorySave(self,
                                            startTime: datetime,
                                            endTime: datetime,
                                            predictCycleTime: float | int,
                                            cycleTime: int | float,
                                            lotId: list | None = None,
                                            batchId: str | None = None,
                                            recipe: str | None = None,
                                            type: str | None = None,
                                            typeInfo: dict | None = None,
                                            contextInfo: dict | None = None,
                                            waferCount: int | None = None,
                                            batchCount: int | None = None):
        reqDto = PerformanceOperationRateSaveReqDto(
            eqpModule=self.module,
            startTime=startTime.isoformat(),
            endTime=endTime.isoformat(),
            predictCycleTime=predictCycleTime,
            cycleTime=cycleTime,
            lotId=lotId,
            batchId=batchId,
            recipe=recipe,
            type=type,
            typeInfo=typeInfo,
            contextInfo=contextInfo,
            waferCount=waferCount,
            batchCount=batchCount,
        )
        OperationRateUseCase.performanceOperationRateSave(reqDto)


class CapaAPIModule:
    def __init__(self, module: int) -> None:
        self.module = module

    def getCycleTime(self, eqpCode: str, recipe: str, type: str | None = None):
        reqDto = CycleTimeReqDto(
            recipe=recipe,
            type=type,
            eqpModule__eqp__code=eqpCode
        )
        result = CapaUseCase.getCycleTime(reqDto)
        if result.__len__() > 0:
            return result[0]
        return None


class Context:
    def __init__(self) -> None:
        self.debugMsgs = []
        super().__init__()
        self.__message = None
        self.mp = {}
        self.event = {}
        self.alarm = {}
        self.trace = {}
        self.conditions = {}
        self.spc = None
        self.etc = {}
        self.contextHistory = list()
        self.currentFdcDataGroup: Optional[ObjectId] = None
        self.__acpSetting = None
        self.__eqpCode = None
        self.__eqpName = None
        self.__moduleName = None
        self.__moduleCode = None
        self.__operationAPIModule = None
        self.__capaAPIModule = None

    def setLogger(self, logger):
        self.logger = logger

    def logMessage(self, message: str):
        self.logger.info(message)

    def get_simpleContext(self) -> Dict:
        return {"MP": self.mp, "conditions": self.conditions}

    def getTraceValue(self, traceGroup, traceName):
        if traceGroup in self.trace.keys() and traceName in self.trace[traceGroup].keys():
            return self.trace.get(traceGroup).get(traceName)
        else:
            return None

    def getEventValue(self, eventGroup, eventName):
        if eventGroup in self.event.keys() and eventName in self.event[eventGroup].keys():
            return self.event.get(eventGroup).get(eventName)
        else:
            return None

    def getAlarmValue(self, alarmGroup, alarmName):
        if alarmGroup in self.alarm.keys() and alarmName in self.alarm[alarmGroup].keys():
            return self.alarm.get(alarmGroup).get(alarmName)
        else:
            return None

    def getConditionsValue(self, conditionsName):
        if conditionsName in self.conditions.keys():
            return self.conditions.get(conditionsName)
        else:
            return None

    def get_message(self):
        return self.__message

    def set_message(self, value: str):
        self.__message = value

    def debug(self, msg: str):
        self.debugMsgs.append(msg)

    def setAPCMessageCoreSetting(self, apcSetting: ACPMessageCoreSettingResDto):
        self.__acpSetting = apcSetting

    def sendACPMessage(self, msg: str):
        if not self.__acpSetting:
            return
        acpBroker = ESBBrokerManager().getACPBroker(self.__acpSetting)
        acpBroker.sendMessage(msg)

    def setEqpCode(self, eqpCode: str):
        self.__eqpCode = eqpCode

    def getEqpCode(self):
        return self.__eqpCode

    def setEqpName(self, eqpName: str):
        self.__eqpName = eqpName

    def getEqpName(self):
        return self.__eqpName

    def setModuleName(self, moduleName: str):
        self.__moduleName = moduleName

    def getModuleName(self):
        return self.__moduleName

    def setModuleCode(self, moduleCode: str):
        self.__moduleCode = moduleCode

    def getModuleCode(self):
        return self.__moduleCode

    def setSPCData(self, spc: dict | None):
        self.spc = spc

    def getSPCData(self):
        return self.spc

    def setOperationAPIModule(self, apiModule: OperationAPIModule):
        self.__operationAPIModule = apiModule

    def getOperationAPIModule(self):
        return self.__operationAPIModule

    def setCapaAPIModule(self, apiModule: CapaAPIModule):
        self.__capaAPIModule = apiModule

    def getCapaAPIModule(self):
        return self.__capaAPIModule
