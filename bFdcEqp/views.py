from django.shortcuts import render

# Create your views here.
from typing import List

from bFdcEqp.Dto.FdcEqpLogicReqDto import FdcEqpLogicReqDto
from bFdcEqp.Dto.FdcEqpLogicResDto import FdcEqpLogicResDto
from bFdcEqp.Dto.FdcEqpReqDto import FdcEqpReqDto
import environ
import requests

from bFdcEqp.Dto.FdcEqpResDto import FdcEqpResDto

env = environ.Env()


# Create your views here.
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

