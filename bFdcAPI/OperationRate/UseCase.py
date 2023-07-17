import dataclasses

import requests
from bFdcAPI import env
from bFdcAPI.OperationRate.Dto.ModuleStateContextInfoUpdateReqDto import ModuleStateContextInfoUpdateReqDto
from bFdcAPI.OperationRate.Dto.ModuleStateDisplayInfoUpdateReqDto import ModuleStateDisplayInfoUpdateReqDto
from bFdcAPI.OperationRate.Dto.ModuleStateUpdateReqDto import ModuleStateUpdateReqDto


class OperationRateUseCase:
    @staticmethod
    def moduleStateUpdate(reqDto: ModuleStateUpdateReqDto):
        requests.post(f"{env('BFDC_URL')}/operationRate/moduleStateUpdate/", json=reqDto.__dict__)

    @staticmethod
    def moduleStateDisplayInfoUpdate(reqDto: ModuleStateDisplayInfoUpdateReqDto):
        requests.post(f"{env('BFDC_URL')}/operationRate/moduleStateDisplayInfoUpdate", json=reqDto.__dict__)

    @staticmethod
    def moduleStateContextInfoUpdate(reqDto: ModuleStateContextInfoUpdateReqDto):
        requests.post(f"{env('BFDC_URL')}/operationRate/moduleStateContextInfoUpdate", json=reqDto.__dict__)
