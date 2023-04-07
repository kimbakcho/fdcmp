import logging
import traceback

from mcp.Process.Enum import FabGroupType
from mcp.Process.MCPEqpEvent import MCPEqpEvent
from mcp.Process.MCPEqpModule import MCPEqpModule
from FDCContext.context import Context, MpBasic, ConditionsBasic

from datetime import datetime

from mcp.Process.McpEqpTraceGroup import McpEqpTraceGroup
import copy

from mcp.models import EventHistory, FdcDataGroup, TraceData

from pytz import timezone

from fdcmp import settings


class McpWorker:

    def __init__(self) -> None:
        super().__init__()
        self.__maxHistorySize = 20
        self.__contextHistory = list()

    def run(self, eqpModule: MCPEqpModule, context: Context):
        try:
            event = None
            traceGroup = None
            if context.mp[MpBasic.IsEvent.value] \
                    and context.mp[MpBasic.EventCode.value] in eqpModule.getEvents().keys():
                event = eqpModule.getEvents()[context.mp[MpBasic.EventCode.value]]
                for logicItem in event.getLogics(event.id):
                    exec(logicItem.logicComPile, None, locals())
                    runResult = locals().get("run")(context)
                    if event.name not in context.event.keys():
                        context.event[event.name] = {}
                    context.event[event.name][logicItem.name] = runResult
            if context.mp[MpBasic.IsTrace.value] and context.mp[
                MpBasic.TraceGroupCode.value] in eqpModule.getTraceGroup().keys():
                traceGroup = eqpModule.getTraceGroup()[context.mp[MpBasic.TraceGroupCode.value]]
                for logicItem in traceGroup.getTraceLogic():
                    exec(logicItem.logicComPile, None, locals())
                    runResult = locals().get("run")(context)
                    if traceGroup.name not in context.trace.keys():
                        context.trace[traceGroup.name] = {}
                    context.trace[traceGroup.name][logicItem.name] = runResult
            for conditions in eqpModule.getConditions():
                exec(conditions.logicComPile, None, locals())
                runResult = locals().get("run")(context)
                context.conditions[conditions.name] = runResult
            if self.__contextHistory.__len__() >= self.__maxHistorySize:
                self.__contextHistory.pop(0)
            self.mcpSaveWork(eqpModule, context, event, traceGroup, self.__contextHistory)
            self.__contextHistory.append(copy.deepcopy(context))
        except Exception as e:
            logger = logging.getLogger('mpl')
            logger.error(e.__str__())
            logger.error(traceback.format_stack())
            traceback.print_stack()

    def isRunStateChange(self, contextHistory: list[Context], context) -> bool:
        return (contextHistory.__len__() > 0 and (
                contextHistory[-1].conditions[ConditionsBasic.IsRun.value]
                != context.conditions[ConditionsBasic.IsRun.value])) \
            or (contextHistory.__len__() == 0)

    def mcpSaveWork(self, eqpModule: MCPEqpModule, context: Context,
                    event: None | MCPEqpEvent,
                    traceGroup: None | McpEqpTraceGroup,
                    contextHistory: list[Context]):

        now = datetime.now(tz=timezone(settings.TIME_ZONE))
        saveTrace = {}
        if traceGroup is not None:
            for traceKey in traceGroup.getTraceLVs().keys():
                if traceGroup.getTraceLVs().get(traceKey).isSave:
                    traceItem = context.trace.get(traceGroup.name).get(traceKey)
                    saveTrace.setdefault(traceKey, traceItem)
        saveEvent = {}
        if event is not None:
            for eventLVKey in event.getEventLVs().keys():
                if event.getEventLVs().get(eventLVKey).isSave:
                    eventItem = context.event.get(event.name).get(eventLVKey)
                    saveEvent.setdefault(eventLVKey, eventItem)

        if self.isRunStateChange(contextHistory, context) \
                and context.conditions[ConditionsBasic.IsRun.value]:
            if context.currentFdcDataGroup is not None:
                ##Idle Fab Group End
                self.fabDataGroupEnd(context, now)
            self.fabDataGroupStart(eqpModule, context, now, FabGroupType.Run)

        if event is not None:
            EventHistory.objects.create(eventCode=context.mp[MpBasic.EventCode.value],
                                        eventName=event.name,
                                        eqpId=eqpModule.eqp,
                                        eqpName=eqpModule.eqpName,
                                        eqpCode=context.mp[MpBasic.EqpCode.value],
                                        eqpModuleId=eqpModule.id,
                                        eqpModuleName=eqpModule.name,
                                        updateTime=now,
                                        value=saveEvent,
                                        context=context.get_simpleContext(),
                                        fdcDataGroup=context.currentFdcDataGroup)
        if context.conditions[ConditionsBasic.IsRun.value]:
            if traceGroup is not None:
                TraceData.objects.create(
                    traceGroupCode=context.mp[MpBasic.TraceGroupCode.value],
                    traceGroupName=traceGroup.name,
                    value=saveTrace,
                    eqpId=eqpModule.eqp,
                    eqpName=eqpModule.eqpName,
                    eqpCode=context.mp[MpBasic.EqpCode.value],
                    eqpModuleId=eqpModule.id,
                    context=context.get_simpleContext(),
                    updateTime=now,
                    fdcDataGroup=context.currentFdcDataGroup
                )

        if self.isRunStateChange(contextHistory, context) and not context.conditions[ConditionsBasic.IsRun.value]:
            self.fabDataGroupEnd(context, now)
            # IdleFabGroupStart
            self.fabDataGroupStart(eqpModule, context, now, FabGroupType.Idle)

    def fabDataGroupStart(self, eqpModule: MCPEqpModule, context: Context,
                          now: datetime, groupType: FabGroupType):
        fdcDataGroup = FdcDataGroup.objects.create(
            eqpModuleName=eqpModule.name,
            eqpModuleId=eqpModule.id,
            context=context.get_simpleContext(),
            eqpId=eqpModule.eqp,
            eqpName=eqpModule.eqpName,
            eqpCode=context.mp[MpBasic.EqpCode.value],
            groupType=groupType.value,
            startTime=now,
            etc=context.etc
        )
        context.currentFdcDataGroup = fdcDataGroup._id

    def fabDataGroupEnd(self, context: Context, now: datetime):
        if context.currentFdcDataGroup is not None:
            fdcDataGroup = FdcDataGroup.objects.get(_id=context.currentFdcDataGroup)
            fdcDataGroup.context = context.get_simpleContext()
            fdcDataGroup.etc = context.etc
            fdcDataGroup.endTime = now
            fdcDataGroup.betweenTimeSec = (fdcDataGroup.endTime - fdcDataGroup.startTime).seconds
            fdcDataGroup.save()
            context.currentFdcDataGroup = None
