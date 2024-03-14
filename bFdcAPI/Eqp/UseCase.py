from typing import List

from bFdcAPI.Eqp.Dto.FdcEqp import FdcEqpResDto, FdcEqpReqDto
from bFdcAPI.Eqp.Dto.FdcEqpModule import FdcEqpModuleResDto, FdcEqpModuleReqDto

import requests

from bFdcAPI import env


class FdcEqpUseCase:
    @staticmethod
    def getEqpList(reqDto: FdcEqpReqDto) -> List[FdcEqpResDto]:
        res = requests.get(f"{env('BFDC_URL')}/eqp/eqp/", params=reqDto.__dict__, timeout=30)
        result = list()
        for item in res.json():
            result.append(FdcEqpResDto(**item))
        return result

    @staticmethod
    def getEqp(id: int) -> FdcEqpResDto:
        res = requests.get(f"{env('BFDC_URL')}/eqp/eqp/{id}/", timeout=30)
        return FdcEqpResDto(**res.json())

    @staticmethod
    def getEqpFromCode(code: str) -> FdcEqpResDto | None:
        res = requests.get(f"{env('BFDC_URL')}/eqp/eqps/", params={
            "code": code
        }, timeout=30)
        json = res.json()
        if json.__len__() == 0:
            return None
        else:
            return FdcEqpResDto(**json[0])

    @staticmethod
    def getEqpModuleList(reqDto: FdcEqpModuleReqDto) -> List[FdcEqpModuleResDto]:
        res = requests.get(f"{env('BFDC_URL')}/eqp/module/", params=reqDto.__dict__, timeout=30)
        result = list()
        for item in res.json():
            result.append(FdcEqpModuleResDto(**item))
        return result

    @staticmethod
    def getEqpModule(id) -> FdcEqpModuleResDto:
        res = requests.get(f"{env('BFDC_URL')}/eqp/module/{id}/", timeout=30)
        return FdcEqpModuleResDto(**res.json())
