from typing import List

import requests

from bFdcAPI import env
from bFdcAPI.ACP.Dto.ACPAlarmGroup import ACPAlarmGroupResDto
from bFdcAPI.ACP.Dto.ACPEQPAlarmGroup import ACPEQPAlarmGroupResDto
from bFdcAPI.ACP.Dto.ACPLogicCode import ACPLogicCodeResDto

class ACPUseCase:

    @staticmethod
    def getACPLogicCode() -> ACPLogicCodeResDto:
        r = requests.get(f"{env('BFDC_URL')}/acp/code/")
        res = r.json()
        return ACPLogicCodeResDto(**res)

    @staticmethod
    def getACPEQPAlarmGroups(eqpCode: str) -> List[ACPEQPAlarmGroupResDto]:
        r = requests.get(f"{env('BFDC_URL')}/acp/eqpAlarmGroups/", params={
            "eqp__code": eqpCode
        })
        result = list()
        for item in r.json():
            result.append(ACPEQPAlarmGroupResDto(**item))
        return result

    @staticmethod
    def getACPAlarmGroup(groupName: str) -> ACPAlarmGroupResDto | None:
        r = requests.get(f"{env('BFDC_URL')}/acp/alarmGroups/", params={
            "groupName": groupName
        })
        res = r.json()
        if res.__len__() == 0:
            return None
        return ACPAlarmGroupResDto(**res[0])

    @staticmethod
    def AcpRun(data: dict):
        requests.post(f"{env('BFDC_URL')}/acp/acpRun/", json=data)




