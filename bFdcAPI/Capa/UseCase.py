import json

import requests

from bFdcAPI import env
from bFdcAPI.Capa.Dto.CycleTime import CycleTimeUpdateReqDto, CycleTimeReqDto, CycleTimeManagerResDto
from bFdcAPI.Capa.Dto.PredictLogic import PredictLogicResDto
from bFdcAPI.Capa.Dto.TrainValidData import TrainValidDataResDto, TrainValidDataUpdateReqDto
from bFdcAPI.Capa.Dto.PredictParamInfo import PredictParamInfoResDto, PredictParamInfoUpdateReqDto
from bFdcAPI.Capa.Dto.TrainLogic import TrainLogicResDto, TrainLogicUpdateReqDto
from bFdcAPI.Capa.Dto.TrainSchedulerHistory import TrainSchedulerHistoryListReqDto, TrainSchedulerHistoryResDto


class CapaUseCase:
    @staticmethod
    def getTrainValidData(eqpModuleId: int) -> TrainValidDataResDto | None:
        r = requests.get(f"{env('BFDC_URL')}/capa/trainValidDataForEqpModule/", params={
            "eqpModule": eqpModuleId
        })

        if not r.ok:
            return None
        return TrainValidDataResDto(**r.json())

    @staticmethod
    def updateTrainValidData(reqDto: TrainValidDataUpdateReqDto) -> TrainValidDataResDto:
        r = requests.patch(f"{env('BFDC_URL')}/capa/trainValidData/{reqDto.id}/", reqDto.__dict__)
        return TrainValidDataResDto(**r.json())

    @staticmethod
    def saveTrainValidData(reqDto: TrainValidDataUpdateReqDto):
        requests.post(f"{env('BFDC_URL')}/capa/trainValidDataSave/", json=reqDto.__dict__)

    @staticmethod
    def getPredictParamInfo(eqpModuleId: int) -> PredictParamInfoResDto | None:
        r = requests.get(f"{env('BFDC_URL')}/capa/predictParamInfoForEqpModule/", params={
            "eqpModule": eqpModuleId
        })
        if not r.ok:
            return None
        return PredictParamInfoResDto(**r.json())

    @staticmethod
    def updatePredictParamInfo(reqDto: PredictParamInfoUpdateReqDto) -> PredictParamInfoResDto:
        r = requests.patch(f"{env('BFDC_URL')}/capa/predictParamInfo/{reqDto.id}/", json= reqDto.__dict__)
        return PredictParamInfoResDto(**r.json())

    @staticmethod
    def savePredictParamInfo(reqDto: PredictParamInfoUpdateReqDto) :
        requests.post(f"{env('BFDC_URL')}/capa/predictParamInfoSave/", json= reqDto.__dict__)


    @staticmethod
    def getTrainLogic(eqpModuleId: int) -> TrainLogicResDto | None:
        r = requests.get(f"{env('BFDC_URL')}/capa/trainLogicForEqpModule/", params={
            "eqpModule": eqpModuleId
        })
        if not r.ok:
            return None
        return TrainLogicResDto(**r.json())

    @staticmethod
    def updateTrainLogic(reqDto: TrainLogicUpdateReqDto) -> TrainLogicResDto:
        r = requests.patch(f"{env('BFDC_URL')}/capa/trainLogic/{reqDto.id}/", json=reqDto.__dict__)
        return TrainLogicResDto(**r.json())

    @staticmethod
    def saveTrainLogic(reqDto: TrainLogicUpdateReqDto) :
        requests.post(f"{env('BFDC_URL')}/capa/trainLogicSave/", json=reqDto.__dict__)


    @staticmethod
    def getPredictLogic(eqpModuleId: int) -> PredictLogicResDto:
        r = requests.get(f"{env('BFDC_URL')}/capa/predictLogicForEqpModule/", params={
            "eqpModule": eqpModuleId
        })
        return PredictLogicResDto(**r.json())

    @staticmethod
    def getTrainSchedulerHistoryList(reqDto: TrainSchedulerHistoryListReqDto) -> list[TrainSchedulerHistoryResDto]:
        r = requests.get(f"{env('BFDC_URL')}/capa/trainSchedulerHistory/", params=reqDto.__dict__)
        result = list()
        for item in r.json()["results"]:
            result.append(TrainSchedulerHistoryResDto(**item))
        return result

    @staticmethod
    def updateTrainSchedulerHistory(reqDto: dict):
        r = requests.patch(f"{env('BFDC_URL')}/capa/trainSchedulerHistory/{reqDto['id']}/",json=reqDto)
        return TrainSchedulerHistoryResDto(**r.json())

    @staticmethod
    def setupNextScheduler(eqpModule: int):
        requests.post(f"{env('BFDC_URL')}/capa/setupNextScheduler/", {
            "eqpModule": eqpModule
        })

    @staticmethod
    def updateCycleTime(reqDto: CycleTimeUpdateReqDto):
        requests.post(f"{env('BFDC_URL')}/capa/cycleTimeUpdate/",json= reqDto.__dict__)

    @staticmethod
    def getCycleTime(reqDto: CycleTimeReqDto):
        r = requests.get(f"{env('BFDC_URL')}/capa/cycleTimes/", params=reqDto.__dict__)
        result = list()
        for item in r.json():
            result.append(CycleTimeManagerResDto(**item))
        return result