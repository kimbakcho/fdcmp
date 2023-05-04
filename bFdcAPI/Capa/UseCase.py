import json

import requests

from bFdcAPI import env
from bFdcAPI.Capa.Dto.CapaValidData import CapaValidDataResDto
from bFdcAPI.Capa.Dto.PredictParamInfo import PredictParamInfoResDto
from bFdcAPI.Capa.Dto.TrainLogic import TrainLogicResDto
from bFdcAPI.Capa.Dto.TrainSchedulerHistory import TrainSchedulerHistoryListReqDto, TrainSchedulerHistoryResDto


class CapaUseCase:
    @staticmethod
    def getTrainValidData(eqpModuleId: int) -> CapaValidDataResDto | None:
        r = requests.get(f"{env('BFDC_URL')}/capa/trainValidDataForEqpModule/", params={
            "eqpModule": eqpModuleId
        })
        if not r.ok:
            return None
        return CapaValidDataResDto(**r.json())

    @staticmethod
    def getPredictParamInfo(eqpModuleId: int) -> PredictParamInfoResDto | None:
        r = requests.get(f"{env('BFDC_URL')}/capa/predictParamInfoForEqpModule/", params={
            "eqpModule": eqpModuleId
        })
        if not r.ok:
            return None
        return PredictParamInfoResDto(**r.json())

    @staticmethod
    def getTrainLogic(eqpModuleId: int) -> TrainLogicResDto | None:
        r = requests.get(f"{env('BFDC_URL')}/capa/trainLogicForEqpModule/", params={
            "eqpModule": eqpModuleId
        })
        if not r.ok:
            return None
        return TrainLogicResDto(**r.json())

    @staticmethod
    def getTrainSchedulerHistoryList(reqDto: TrainSchedulerHistoryListReqDto) -> list[TrainSchedulerHistoryResDto]:
        r = requests.get(f"{env('BFDC_URL')}/capa/trainSchedulerHistory/", params=reqDto.__dict__)
        result = list()
        for item in r.json()["results"]:
            result.append(TrainSchedulerHistoryResDto(**item))
        return result