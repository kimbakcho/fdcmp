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
    def getEqp(id: int) -> FdcEqpResDto:
        res = requests.get(f"{env('BFDC_URL')}/eqp/eqp/{id}/")
        return FdcEqpResDto(**res.json())

    @staticmethod
    def getEqpFromCode(code: str) -> FdcEqpResDto | None:
        res = requests.get(f"{env('BFDC_URL')}/eqp/eqps/", params={
            "code": code
        })
        json = res.json()
        if json.__len__() == 0:
            return None
        else:
            return FdcEqpResDto(**json[0])

    @staticmethod
    def getEqpLogicList(reqDto: FdcEqpLogicReqDto) -> List[FdcEqpLogicResDto]:
        res = requests.get(f"{env('BFDC_URL')}/eqp/eqpLogic/", params=reqDto.__dict__)
        result = list()
        for item in res.json():
            result.append(FdcEqpLogicResDto(**item))
        return result

    @staticmethod
    def getEqpModuleList(reqDto: FdcEqpModuleReqDto) -> List[FdcEqpModuleResDto]:
        res = requests.get(f"{env('BFDC_URL')}/eqp/module/", params=reqDto.__dict__)
        result = list()
        for item in res.json():
            result.append(FdcEqpModuleResDto(**item))
        return result

    @staticmethod
    def getEqpModule(id) -> FdcEqpModuleResDto:
        res = requests.get(f"{env('BFDC_URL')}/eqp/module/{id}/")
        return FdcEqpModuleResDto(**res.json())
