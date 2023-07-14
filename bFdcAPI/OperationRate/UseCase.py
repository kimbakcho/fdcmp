import requests
from bFdcAPI import env
from bFdcAPI.OperationRate.Dto.ModuleStateUpdateReqDto import ModuleStateUpdateReqDto


class OperationRateUseCase:
    @staticmethod
    def moduleStateUpdate(reqDto: ModuleStateUpdateReqDto):
        requests.post(f"{env('BFDC_URL')}/operationRate/moduleStateUpdate/", reqDto)
