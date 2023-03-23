import requests

from bFdc.MCP.Dto.FdcMcpConditions import ConditionsResDto
from bFdc.MCP.Dto.FdcMcpEvent import FdcMcpEventResDto
from bFdc.MCP.Dto.FdcMcpEventLV import FdcMcpEventLVResDto
from bFdc.MCP.Dto.FdcMcpTraceGroup import FdcMcpTraceGroupResDto
from bFdc.MCP.Dto.FdcMcpTraceLV import TraceLVResDto
from bFdc import env

class FdcMcpUseCase:
    @staticmethod
    def getEventList(eqpModule: int) -> list[FdcMcpEventResDto]:
        res = requests.get(f"{env('BFDC_URL')}/mcp/event/", params={"eqpModule": eqpModule})
        result: list[FdcMcpEventResDto] = list()
        for item in res.json():
            result.append(FdcMcpEventResDto(**item))
        return result

    @staticmethod
    def getEventLVList(event: int) -> list[FdcMcpEventLVResDto]:
        res = requests.get(f"{env('BFDC_URL')}/mcp/eventLV/", params={"event": event})
        result: list[FdcMcpEventLVResDto] = list()
        for item in res.json():
            result.append(FdcMcpEventLVResDto(**item))
        return result

    @staticmethod
    def getTraceGroupList(eqpModule: int) -> list[FdcMcpTraceGroupResDto]:
        res = requests.get(f"{env('BFDC_URL')}/mcp/traceGroup/", params={"eqpModule": eqpModule})
        result: list[FdcMcpTraceGroupResDto] = list()
        for item in res.json():
            result.append(FdcMcpTraceGroupResDto(**item))
        return result

    @staticmethod
    def getTraceLVList(traceGroup: int) -> list[TraceLVResDto]:
        res = requests.get(f"{env('BFDC_URL')}/mcp/traceLV/", params={"traceGroup": traceGroup})
        result: list[TraceLVResDto] = list()
        for item in res.json():
            result.append(TraceLVResDto(**item))
        return result

    @staticmethod
    def getConditions(eqpModule: int):
        res = requests.get(f"{env('BFDC_URL')}/mcp/conditions/", params={"eqpModule": eqpModule})
        result: list[ConditionsResDto] = list()
        for item in res.json():
            result.append(ConditionsResDto(**item))
        return result
