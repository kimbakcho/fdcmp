from typing import List

from bFdc.Eqp.Dto.FdcEqpLogic import FdcEqpLogicReqDto, FdcEqpLogicResDto

from bFdc.Eqp.Dto.FdcEqp import FdcEqpResDto, FdcEqpReqDto
from bFdc.Eqp.Dto.FdcEqpModule import FdcEqpModuleResDto, FdcEqpModuleReqDto

import requests
from bFdc.Eqp import env


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
