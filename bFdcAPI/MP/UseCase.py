from typing import List

import requests
from bFdcAPI import env
from bFdcAPI.MP.Dto.Core import CoreResDto
from bFdcAPI.MP.Dto.MLB import MLBResDto
from bFdcAPI.MP.Dto.MPL import MPLResDto




class FdcMpUseCase:
    @staticmethod
    def getMPL() -> List[MPLResDto]:
        r = requests.get(f"{env('BFDC_URL')}/mp/mpl/", timeout=30)
        result = list()
        for item in r.json():
            result.append(MPLResDto(**item))
        return result

    @staticmethod
    def getMLB(id: int) -> MLBResDto:
        r = requests.get(f"{env('BFDC_URL')}/mp/mlb/{id}/", timeout=30)
        return MLBResDto(**r.json())

    @staticmethod
    def getCoreList() -> List[CoreResDto]:
        r = requests.get(f"{env('BFDC_URL')}/mp/core/", timeout=30)
        result = list()
        for item in r.json():
            result.append(CoreResDto(**item))
        return result

    @staticmethod
    def getCore(id: int) -> CoreResDto:
        r = requests.get(f"{env('BFDC_URL')}/mp/core/{id}", timeout=30)
        return CoreResDto(**r.json())
