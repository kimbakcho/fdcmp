import json
import logging
import traceback

import requests

from ESB.ESBBrokerManager import ESBBrokerManager
from bFdcAPI.ACP.UseCase import ACPUseCase
from wRecipeInterLock.bFdcAPI.Dto.RecipeInterLockEqpModule import RecipeInterLockEqpModuleReqDto
from wRecipeInterLock.bFdcAPI.Dto.RecipeInterLockRecipe import RILRecipeQuickSearchReqDto
from wRecipeInterLock.bFdcAPI.UseCase import WRecipeInterLockUseCase


class WRILWorker:

    def __init__(self) -> None:
        super().__init__()
        self.loggerWRIL = logging.getLogger('wRIL')
        setting = ACPUseCase.getACPMessageCoreSetting()
        self.acpBroker = ESBBrokerManager().getACPBroker(setting)

    def messageParser(self, message: str):
        try:
            message = json.loads(message)

            module = WRecipeInterLockUseCase.getRILModule(RecipeInterLockEqpModuleReqDto(
                eqpCode=message["eqpCode"],
                moduleCode=message["moduleCode"]
            ))

            # WRIL 시스템에 등록된 모듈(챔버)만 HOLD을 잡는것을 한다.
            if module.__len__() > 0:
                rilRecipe = WRecipeInterLockUseCase.getRILRecipeQuickSearch(
                    RILRecipeQuickSearchReqDto(eqpCode=message["eqpCode"], moduleCode=message["moduleCode"],
                                               operationCode=message["operationCode"], recipeName=message["recipe"]))

                if rilRecipe is None:
                    self.loggerWRIL.info(message)
                    cause = "모듈에 등록 되지 않은 레시피가 진행되었습니다."
                    self.loggerWRIL.info(cause)
                    message.get("lotId", "")
                    operationInfo = requests.get("http://10.20.10.114/mesapi/mes/operationInfo/", params={
                        "operationCode": message.get("operationCode", "")
                    })
                    operationInfo = operationInfo.json()
                    self.acpBroker.sendMessage(json.dumps({
                        "from": "WRIL",
                        "eqpCode": message.get("eqpCode", ""),
                        "moduleCode": message.get("moduleCode", ""),
                        "operationCode": message.get("operationCode", ""),
                        "operationName": operationInfo.get("operationName",""),
                        "eqpName": module[0].eqpName,
                        "moduleName": module[0].moduleName,
                        "alarmAction": ["sms", "email", "eqpLock"],
                        "cause": cause
                    }))
                    return

                if rilRecipe.useParamInterLock:
                    for item in rilRecipe.paramInterLock:
                        if item["paramName"] in message.keys():
                            if message[item["paramName"]] != item["paramValue"]:
                                self.loggerWRIL.info(message)
                                cause = f"레시피의 {item['paramName']} =" \
                                        f"{item['paramValue']}({message[item['paramName']]}) 일치 하지 않습니다."
                                self.loggerWRIL.info(cause)
                                self.acpBroker.sendMessage(json.dumps({
                                    "from": "WRIL",
                                    "eqpCode": message.get("eqpCode", ""),
                                    "moduleCode": message.get("moduleCode", ""),
                                    "recipe": message.get("recipe", ""),
                                    "eqpName": module[0].eqpName,
                                    "moduleName": module[0].moduleName,
                                    "operationCode": message.get("operationCode", ""),
                                    "operationName": rilRecipe.operationName,
                                    "alarmAction": ["sms", "email", "eqpLock"],
                                    "lotId": message.get("lotId", ""),
                                    "product": message.get("product", ""),
                                    "cause": cause
                                }))
                                return
                        else:
                            self.loggerWRIL.info(message)
                            cause = f"레시피의 {item['paramName']}) 이 없습니다."
                            self.loggerWRIL.info(cause)
                            self.acpBroker.sendMessage(json.dumps({
                                "from": "WRIL",
                                "eqpCode": message["eqpCode"],
                                "moduleCode": message["moduleCode"],
                                "recipe": message["recipe"],
                                "eqpName": module[0].eqpName,
                                "moduleName": module[0].moduleName,
                                "operationCode": message["operationCode"],
                                "operationName": rilRecipe.operationName,
                                "alarmAction": ["sms", "email", "eqpLock"],
                                "lotId": message.get("lotId", ""),
                                "product": message.get("product", ""),
                                "cause": cause
                            }))
                            return


        except Exception as e:
            self.loggerWRIL.error(message)
            self.loggerWRIL.error(traceback.format_exc())
            self.loggerWRIL.error(e.__str__())
            self.loggerWRIL.error(traceback.format_stack())
            traceback.print_stack()

    def commandParser(self, message: str):
        pass
