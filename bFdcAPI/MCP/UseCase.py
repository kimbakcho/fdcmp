from typing import List

import requests

from bFdcAPI.MCP.Dto.FdcMcpAlarm import FdcMcpAlarmResDto
from bFdcAPI.MCP.Dto.FdcMcpAlarmLV import FdcMcpAlarmLVResDto
from bFdcAPI.MCP.Dto.FdcMcpConditions import ConditionsResDto
from bFdcAPI.MCP.Dto.FdcMcpEvent import FdcMcpEventResDto
from bFdcAPI.MCP.Dto.FdcMcpEventLV import FdcMcpEventLVResDto
from bFdcAPI.MCP.Dto.FdcMcpThread import ThreadingLoopResDto
from bFdcAPI.MCP.Dto.FdcMcpTraceGroup import FdcMcpTraceGroupResDto
from bFdcAPI.MCP.Dto.FdcMcpTraceLV import TraceLVResDto

from bFdcAPI import env


class FdcMcpUseCase:

    @staticmethod
    def getInitList(eqpModule: int) -> List[dict]:
        res = requests.get(f"{env('BFDC_URL')}/mcp/init/", params={"eqpModule": eqpModule}, timeout=30)
        return res.json()
    @staticmethod
    def getEventList(eqpModule: int) -> List[FdcMcpEventResDto]:

        res = requests.get(f"{env('BFDC_URL')}/mcp/event/", params={"eqpModule": eqpModule}, timeout=30)
        result: list[FdcMcpEventResDto] = list()
        for item in res.json():
            result.append(FdcMcpEventResDto(**item))
        return result

    @staticmethod
    def getEventLVList(event: int) -> List[FdcMcpEventLVResDto]:
        res = requests.get(f"{env('BFDC_URL')}/mcp/eventLV/", params={"event": event}, timeout=30)
        result: list[FdcMcpEventLVResDto] = list()
        for item in res.json():
            result.append(FdcMcpEventLVResDto(**item))
        return result

    @staticmethod
    def getAlarmList(eqpModule: int) -> List[FdcMcpAlarmResDto]:
        res = requests.get(f"{env('BFDC_URL')}/mcp/alarm/", params={"eqpModule": eqpModule}, timeout=30)
        result: list[FdcMcpAlarmResDto] = list()
        for item in res.json():
            result.append(FdcMcpAlarmResDto(**item))
        return result

    @staticmethod
    def getAlarmLVList(alarm: int) -> List[FdcMcpAlarmLVResDto]:
        res = requests.get(f"{env('BFDC_URL')}/mcp/alarmLV/", params={"alarm": alarm}, timeout=30)
        result: list[FdcMcpAlarmLVResDto] = list()
        for item in res.json():
            result.append(FdcMcpAlarmLVResDto(**item))
        return result

    @staticmethod
    def getTraceGroupList(eqpModule: int) -> List[FdcMcpTraceGroupResDto]:
        res = requests.get(f"{env('BFDC_URL')}/mcp/traceGroup/", params={"eqpModule": eqpModule}, timeout=30)
        result: list[FdcMcpTraceGroupResDto] = list()
        for item in res.json():
            result.append(FdcMcpTraceGroupResDto(**item))
        return result

    @staticmethod
    def getTraceLVList(traceGroup: int) -> List[TraceLVResDto]:
        res = requests.get(f"{env('BFDC_URL')}/mcp/traceLV/", params={"traceGroup": traceGroup}, timeout=30)
        result: list[TraceLVResDto] = list()
        for item in res.json():
            result.append(TraceLVResDto(**item))
        return result

    @staticmethod
    def getConditions(eqpModule: int):
        res = requests.get(f"{env('BFDC_URL')}/mcp/conditions/", params={"eqpModule": eqpModule}, timeout=30)
        result: list[ConditionsResDto] = list()
        for item in res.json():
            result.append(ConditionsResDto(**item))
        return result

    @staticmethod
    def getThreadingLoops(eqpModule: int)->list[ThreadingLoopResDto]:
        res = requests.get(f"{env('BFDC_URL')}/mcp/threadingLoops/", params={"eqpModule": eqpModule}, timeout=30)
        result: list[ThreadingLoopResDto] = list()
        for item in res.json():
            result.append(ThreadingLoopResDto(**item))
        return result

    @staticmethod
    def getThreadingLoop(id: int) -> ThreadingLoopResDto:
        res = requests.get(f"{env('BFDC_URL')}/mcp/threadingLoop/{id}/", timeout=30)
        item = res.json()
        return ThreadingLoopResDto(**item)