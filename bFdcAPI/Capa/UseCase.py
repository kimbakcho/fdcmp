import json

import requests

from bFdcAPI import env
from bFdcAPI.Capa.Dto.PredictLogic import PredictLogicResDto
from bFdcAPI.Capa.Dto.TrainValidData import TrainValidDataResDto, TrainValidDataUpdateReqDto
from bFdcAPI.Capa.Dto.PredictParamInfo import PredictParamInfoResDto, PredictParamInfoUpdateReqDto
from bFdcAPI.Capa.Dto.TrainLogic import TrainLogicResDto, TrainLogicUpdateReqDto
from bFdcAPI.Capa.Dto.TrainSchedulerHistory import TrainSchedulerHistoryListReqDto, TrainSchedulerHistoryResDto, \
    TrainSchedulerHistoryUpdateReqDto


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
    def getPredictParamInfo(eqpModuleId: int) -> PredictParamInfoResDto | None:
        r = requests.get(f"{env('BFDC_URL')}/capa/predictParamInfoForEqpModule/", params={
            "eqpModule": eqpModuleId
        })
        if not r.ok:
            return None
        return PredictParamInfoResDto(**r.json())

    @staticmethod
    def updatePredictParamInfo(reqDto: PredictParamInfoUpdateReqDto) -> PredictParamInfoResDto:
        r = requests.patch(f"{env('BFDC_URL')}/capa/predictParamInfo/{reqDto.id}/",reqDto.__dict__)
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
    def updateTrainLogic(reqDto: TrainLogicUpdateReqDto) -> TrainLogicResDto:
        r = requests.patch(f"{env('BFDC_URL')}/capa/trainLogic/{reqDto.id}/", reqDto.__dict__)
        return TrainLogicResDto(**r.json())

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
    def updateTrainSchedulerHistory(reqDto: TrainSchedulerHistoryUpdateReqDto):
        r = requests.patch(f"{env('BFDC_URL')}/capa/trainSchedulerHistory/{reqDto.id}/", reqDto.__dict__)
        return TrainSchedulerHistoryResDto(**r.json())