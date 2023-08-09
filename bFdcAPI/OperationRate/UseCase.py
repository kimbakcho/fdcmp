import dataclasses

import requests
from bFdcAPI import env
from bFdcAPI.OperationRate.Dto.ModuleStateContextInfoUpdateReqDto import ModuleStateContextInfoUpdateReqDto
from bFdcAPI.OperationRate.Dto.ModuleStateDisplayInfoUpdateReqDto import ModuleStateDisplayInfoUpdateReqDto
from bFdcAPI.OperationRate.Dto.ModuleStateEtcInfoUpdateReqDto import ModuleStateEtcInfoUpdateReqDto
from bFdcAPI.OperationRate.Dto.ModuleStateModifyPlanProductionOutputReqDto import \
    ModuleStateModifyPlanProductionOutputReqDto
from bFdcAPI.OperationRate.Dto.ModuleStatePredictFinishTimeUpdateReqDto import ModuleStatePredictFinishTimeUpdateReqDto
from bFdcAPI.OperationRate.Dto.ModuleStateUpdateReqDto import ModuleStateUpdateReqDto


class OperationRateUseCase:
    @staticmethod
    def moduleStateUpdate(reqDto: ModuleStateUpdateReqDto):
        requests.post(f"{env('BFDC_URL')}/operationRate/moduleStateUpdate/", json=reqDto.__dict__)

    @staticmethod
    def moduleStateDisplayInfoUpdate(reqDto: ModuleStateDisplayInfoUpdateReqDto):
        requests.post(f"{env('BFDC_URL')}/operationRate/moduleStateDisplayInfoUpdate/", json=reqDto.__dict__)

    @staticmethod
    def moduleStateContextInfoUpdate(reqDto: ModuleStateContextInfoUpdateReqDto):
        requests.post(f"{env('BFDC_URL')}/operationRate/moduleStateContextInfoUpdate/", json=reqDto.__dict__)

    @staticmethod
    def moduleStateEtcInfoUpdate(reqDto: ModuleStateEtcInfoUpdateReqDto):
        requests.post(f"{env('BFDC_URL')}/operationRate/moduleStateEtcInfoUpdate/", json=reqDto.__dict__)

    @staticmethod
    def moduleStateAddProductionOutput(reqDto: ModuleStateModifyPlanProductionOutputReqDto):
        requests.post(f"{env('BFDC_URL')}/operationRate/moduleStateAddProductionOutput/", json=reqDto.__dict__)

    @staticmethod
    def moduleStateUpdatePredictFinishTime(reqDto: ModuleStatePredictFinishTimeUpdateReqDto):
        requests.post(f"{env('BFDC_URL')}/operationRate/moduleStateUpdatePredictFinishTime/", json=reqDto.__dict__)