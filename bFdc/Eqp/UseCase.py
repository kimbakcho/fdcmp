from typing import List

from bFdc.Eqp.Dto.FdcEqpLogicReqDto import FdcEqpLogicReqDto
from bFdc.Eqp.Dto.FdcEqpLogicResDto import FdcEqpLogicResDto
from bFdc.Eqp.Dto.FdcEqpReqDto import FdcEqpReqDto
from bFdc.Eqp.Dto.FdcEqpResDto import FdcEqpResDto

from fdcmp.settings import env

import requests


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
