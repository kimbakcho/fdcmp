from typing import List

from bFdcAPI.Eqp.Dto.FdcEqpLogic import FdcEqpLogicReqDto, FdcEqpLogicResDto

from bFdcAPI.Eqp.Dto.FdcEqp import FdcEqpResDto, FdcEqpReqDto
from bFdcAPI.Eqp.Dto.FdcEqpModule import FdcEqpModuleResDto, FdcEqpModuleReqDto

import requests

from bFdcAPI import env


class FdcEqpUseCase:
    @staticmethod
    def getEqpList(reqDto: FdcEqpReqDto) -> List[FdcEqpResDto]:
        res = requests.get(f"{env('BFDC_URL')}/eqp/eqp/", params=reqDto.__dict__)
        result = list()
        for item in res.json():
            result.append(FdcEqpResDto(**item))
        return result

    @staticmethod
    def getEqpLogicList(reqDto: FdcEqpLogicReqDto) -> List[FdcEqpLogicResDto]:
        res = requests.get(f"{env('BFDC_URL')}/eqp/eqpLogic/", params=reqDto.__dict__)
        result = list()
        for item in res.json():
            result.append(FdcEqpLogicResDto(**item))
        return result

    @staticmethod
    def getEqpModuleList(reqDto: FdcEqpModuleReqDto) -> list[FdcEqpModuleResDto]:
        res = requests.get(f"{env('BFDC_URL')}/eqp/module/", params=reqDto.__dict__)
        result = list()
        for item in res.json():
            result.append(FdcEqpModuleResDto(**item))
        return result

    def getEqpModule(self, id) -> FdcEqpModuleResDto:
        res = requests.get(f"{env('BFDC_URL')}/eqp/module/{id}/")
        return FdcEqpModuleResDto(**res.json())
