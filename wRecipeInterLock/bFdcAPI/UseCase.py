import requests
from bFdcAPI import env
from wRecipeInterLock.bFdcAPI.Dto.RecipeInterLockSetting import RecipeInterLockSettingResDto


class WRecipeInterLockUseCase:
    @staticmethod
    def getSetting() -> RecipeInterLockSettingResDto:
        r = requests.get(f"{env('BFDC_URL')}/ril/setting/")
        return RecipeInterLockSettingResDto(**r.json())
