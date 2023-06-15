import json
import logging
import traceback

import requests

from wRecipeInterLock.bFdcAPI.Dto.RecipeInterLockEqpModule import RecipeInterLockEqpModuleReqDto
from wRecipeInterLock.bFdcAPI.Dto.RecipeInterLockRecipe import RILRecipeQuickSearchReqDto
from wRecipeInterLock.bFdcAPI.UseCase import WRecipeInterLockUseCase


class WRILWorker:


    def __init__(self) -> None:
        super().__init__()
        self.loggerWRIL = logging.getLogger('wRIL')

    def messageParser(self, message: str):
        try:
            message = json.loads(message)

            module = WRecipeInterLockUseCase.getRILModule(RecipeInterLockEqpModuleReqDto(
                eqpCode=message["eqpCode"],
                moduleCode=message["moduleCode"]
            ))

            #Todo
            #Lot의 현재 공정을 가지고 온다

            #WRIL 시스템에 등록된 모듈(챔버)만 HOLD을 잡는것을 한다.
            if module.__len__() > 0:
                rilRecipe = WRecipeInterLockUseCase.getRILRecipeQuickSearch(
                    RILRecipeQuickSearchReqDto(eqpCode=message["eqpCode"], moduleCode=message["moduleCode"],
                                               operationCode="OP01002020", recipeName=message["recipe"]))
                if rilRecipe is None:
                    self.loggerWRIL.info("send_recipe don't have")
                    return

                if rilRecipe.useParamInterLock:
                    for item in rilRecipe.paramInterLock:
                        if item["paramName"] in message.keys():
                            if message[item["paramName"]] != item["paramValue"]:
                                self.loggerWRIL.info("send_recipe don't match paramKey")
                                return
                        else:
                            self.loggerWRIL.info("send_recipe don't match paramKey")
                            return


        except Exception as e:
            self.loggerWRIL.error(traceback.format_exc())
            self.loggerWRIL.error(e.__str__())
            self.loggerWRIL.error(traceback.format_stack())
            traceback.print_stack()

    def commandParser(self, message: str):
        pass