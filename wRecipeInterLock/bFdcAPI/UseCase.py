import requests
from bFdcAPI import env
from wRecipeInterLock.bFdcAPI.Dto.RecipeInterLockEqpModule import RecipeInterLockEqpModuleResDto, \
    RecipeInterLockEqpModuleReqDto
from wRecipeInterLock.bFdcAPI.Dto.RecipeInterLockRecipe import RecipeInterLockRecipeResDto, RILRecipeQuickSearchReqDto
from wRecipeInterLock.bFdcAPI.Dto.RecipeInterLockSetting import RecipeInterLockSettingResDto


class WRecipeInterLockUseCase:
    @staticmethod
    def getSetting() -> RecipeInterLockSettingResDto:
        r = requests.get(f"{env('BFDC_URL')}/ril/setting/")
        return RecipeInterLockSettingResDto(**r.json())

    @staticmethod
    def getRILModule(reqDto: RecipeInterLockEqpModuleReqDto) -> list[RecipeInterLockEqpModuleResDto]:
        r = requests.get(f"{env('BFDC_URL')}/ril/modules/", params={
            "RILEqp__eqp__code": reqDto.eqpCode,
            "module__code": reqDto.moduleCode
        })
        result = list()
        for item in r.json():
            result.append(RecipeInterLockEqpModuleResDto(**item))
        return result

    @staticmethod
    def getRILRecipeQuickSearch(reqDto: RILRecipeQuickSearchReqDto) -> RecipeInterLockRecipeResDto | None:
        r = requests.get(f"{env('BFDC_URL')}/ril/recipeQuickSearch/", params=reqDto.__dict__)
        if len(r.content) == 0:
            return None
        return RecipeInterLockRecipeResDto(**r.json())
