import requests

from bFdcAPI.MP.Dto.Core import CoreResDto
from bFdcAPI.MP.Dto.MBL import MBLResDto
from bFdcAPI.MP.Dto.MPL import MPLResDto

from bFdcAPI import env


class FdcMpUseCase:
    @staticmethod
    def getMPL() -> list[MPLResDto]:
        r = requests.get(f"{env('BFDC_URL')}/mp/mpl/")
        result = list()
        for item in r.json():
            result.append(MPLResDto(**item))
        return result

    @staticmethod
    def getMLB(id: int) -> MBLResDto:
        r = requests.get(f"{env('BFDC_URL')}/mp/mbl/{id}/")
        return MBLResDto(**r.json())

    @staticmethod
    def getCoreList() -> list[CoreResDto]:
        r = requests.get(f"{env('BFDC_URL')}/mp/core/")
        result = list()
        for item in r.json():
            result.append(CoreResDto(**item))
        return result

    @staticmethod
    def getCore(id: int) -> CoreResDto:
        r = requests.get(f"{env('BFDC_URL')}/mp/core/{id}")
        return CoreResDto(**r.json())