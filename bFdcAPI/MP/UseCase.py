from typing import List

import requests
from bFdcAPI import env
from bFdcAPI.MP.Dto.Core import CoreResDto
from bFdcAPI.MP.Dto.MLB import MLBResDto
from bFdcAPI.MP.Dto.MPL import MPLResDto




class FdcMpUseCase:
    @staticmethod
    def getMPL() -> List[MPLResDto]:
        r = requests.get(f"{env('BFDC_URL')}/mp/mpl/")
        result = list()
        for item in r.json():
            result.append(MPLResDto(**item))
        return result

    @staticmethod
    def getMLB(id: int) -> MLBResDto:
        r = requests.get(f"{env('BFDC_URL')}/mp/mlb/{id}/")
        return MLBResDto(**r.json())

    @staticmethod
    def getCoreList() -> List[CoreResDto]:
        r = requests.get(f"{env('BFDC_URL')}/mp/core/")
        result = list()
        for item in r.json():
            result.append(CoreResDto(**item))
        return result

    @staticmethod
    def getCore(id: int) -> CoreResDto:
        r = requests.get(f"{env('BFDC_URL')}/mp/core/{id}")
        return CoreResDto(**r.json())
