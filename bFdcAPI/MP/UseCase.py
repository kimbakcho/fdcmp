from typing import List

import requests

from bFdcAPI.MP.Dto.Core import CoreResDto
from bFdcAPI.MP.Dto.MBL import MBLResDto
from bFdcAPI.MP.Dto.MPL import MPLResDto

from bFdcAPI import env


class FdcMpUseCase:
    @staticmethod
    def getMPL() -> List[MPLResDto]:
        r = requests.get(f"{env('BFDC_URL')}/mp/mpl/")
        result = list()
        for item in r.json():
            result.append(MPLResDto(**item))
        return result

    @staticmethod
    def getMBL(id: int) -> MBLResDto:
        r = requests.get(f"{env('BFDC_URL')}/mp/mbl/{id}/")
        return MBLResDto(**r.json())

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
