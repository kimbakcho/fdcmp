import requests

from bFdc.MP.Dto.MPLResDto import MPLResDto

from bFdc import env


class FdcMpUseCase:
    @staticmethod
    def getMPL() -> list[MPLResDto]:
        r = requests.get(f"{env('BFDC_URL')}/mp/mpl/")
        result = list()
        for item in r.json():
            result.append(MPLResDto(**item))
        return result
