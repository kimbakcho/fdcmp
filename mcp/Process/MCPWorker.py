import logging
import traceback

from mcp.Process.Enum import FabGroupType
from mcp.Process.MCPEqpAlarm import MCPEqpAlarm
from mcp.Process.MCPEqpEvent import MCPEqpEvent
from mcp.Process.MCPEqpModule import MCPEqpModule
from FDCContext.context import Context, MpBasic, ConditionsBasic

from datetime import datetime

from mcp.Process.MCPEqpTraceGroup import McpEqpTraceGroup
import copy

from mcp.models import EventHistory, FdcDataGroup, TraceData, AlarmHistory

from pytz import timezone

from fdcmp import settings


class McpWorker:

    def __init__(self) -> None:
        super().__init__()
        self.__maxHistorySize = 20

        self.__logger = logging.getLogger('mcp')

    def run(self, eqpModule: MCPEqpModule, context: Context):
        try:
            event = None
            traceGroup = None
            alarm = None
            if context.mp[MpBasic.IsEvent.value] \
                    and context.mp[MpBasic.EventCode.value] in eqpModule.getEvents().keys():
                event = eqpModule.getEvents()[context.mp[MpBasic.EventCode.value]]
                for logicItem in event.getLogics(event.id):
                    try:
                        exec(logicItem.logicComPile, None, locals())
                        runResult = locals().get("run")(context)
                        if event.name not in context.event.keys():
                            context.event[event.name] = {}
                        context.event[event.name][logicItem.name] = runResult
                    except Exception as e:
                        self.__logger.error(context.get_message())
                        self.__logger.error(f'{eqpModule.eqpName}_{eqpModule.name} {logicItem.name}')
                        self.__logger.error(traceback.format_exc())
                        self.__logger.error(e.__str__())
                        self.__logger.error(traceback.format_stack())
                        traceback.print_stack()

            if context.mp[MpBasic.IsAlarm.value] \
                    and context.mp[MpBasic.AlarmCode.value] in eqpModule.getAlarms().keys():
                alarm = eqpModule.getAlarms()[context.mp[MpBasic.AlarmCode.value]]
                for logicItem in alarm.getLogics(alarm.id):
                    try:
                        exec(logicItem.logicComPile, None, locals())
                        runResult = locals().get("run")(context)
                        if alarm.name not in context.alarm.keys():
                            context.alarm[alarm.name] = {}
                        context.alarm[alarm.name][logicItem.name] = runResult
                    except Exception as e:
                        self.__logger.error(context.get_message())
                        self.__logger.error(f'{eqpModule.eqpName}_{eqpModule.name} {logicItem.name}')
                        self.__logger.error(traceback.format_exc())
                        self.__logger.error(e.__str__())
                        self.__logger.error(traceback.format_stack())
                        traceback.print_stack()

            if context.mp[MpBasic.IsTrace.value] \
                    and context.mp[MpBasic.TraceGroupCode.value] in eqpModule.getTraceGroup().keys():
                traceGroup = eqpModule.getTraceGroup()[context.mp[MpBasic.TraceGroupCode.value]]
                for logicItem in traceGroup.getTraceLogic():
                    try:
                        exec(logicItem.logicComPile, None, locals())
                        runResult = locals().get("run")(context)
                        if traceGroup.name not in context.trace.keys():
                            context.trace[traceGroup.name] = {}
                        context.trace[traceGroup.name][logicItem.name] = runResult
                    except Exception as e:
                        self.__logger.error(context.get_message())
                        self.__logger.error(f'{eqpModule.eqpName}_{eqpModule.name} {logicItem.name}')
                        self.__logger.error(traceback.format_exc())
                        self.__logger.error(e.__str__())
                        self.__logger.error(traceback.format_stack())
                        traceback.print_stack()

            for conditions in eqpModule.getConditions():
                try:
                    exec(conditions.logicComPile, None, locals())
                    runResult = locals().get("run")(context)
                    context.conditions[conditions.name] = runResult
                except Exception as e:
                    self.__logger.error(context.get_message())
                    self.__logger.error(f'{eqpModule.eqpName}_{eqpModule.name} {conditions.name}')
                    self.__logger.error(traceback.format_exc())
                    self.__logger.error(e.__str__())
                    self.__logger.error(traceback.format_stack())
                    traceback.print_stack()
            if context.contextHistory.__len__() >= self.__maxHistorySize:
                context.contextHistory.pop(0)
            self.mcpSaveWork(eqpModule, context, event, alarm, traceGroup)
            # If the context object contains a field that cannot be deep copied, it does not become deep copy.
            saveContext = Context()
            saveContext.mp = context.mp
            saveContext.event = context.event
            saveContext.alarm = context.alarm
            saveContext.trace = context.trace
            saveContext.etc = context.etc
            saveContext.conditions = context.conditions
            saveContext.currentFdcDataGroup = context.currentFdcDataGroup

            context.contextHistory.append(copy.deepcopy(saveContext))
        except Exception as e:
            logger = logging.getLogger('mcp')
            logger.error(context.get_message())
            self.__logger.error(f'{eqpModule.eqpName}_{eqpModule.name}')
            logger.error(traceback.format_exc())
            logger.error(e.__str__())
            logger.error(traceback.format_stack())
            traceback.print_stack()

    def isRunStateChange(self, context) -> bool:
        return (context.contextHistory.__len__() > 0 and (
                context.contextHistory[-1].conditions.get(ConditionsBasic.IsRun.value)
                != context.conditions.get(ConditionsBasic.IsRun.value))) \
            or (context.contextHistory.__len__() == 0)

    def mcpSaveWork(self, eqpModule: MCPEqpModule, context: Context,
                    event: None | MCPEqpEvent,
                    alarm: None | MCPEqpAlarm,
                    traceGroup: None | McpEqpTraceGroup):

        now = datetime.now(tz=timezone(settings.TIME_ZONE))
        saveTrace = {}
        if traceGroup is not None:
            for traceKey in traceGroup.getTraceLVs().keys():
                if traceGroup.getTraceLVs().get(traceKey).isSave:
                    traceItem = context.trace.get(traceGroup.name).get(traceKey)
                    saveTrace[traceKey] = traceItem
        saveEvent = {}
        if event is not None:
            for eventLVKey in event.getEventLVs().keys():
                if event.getEventLVs().get(eventLVKey).isSave:
                    eventItem = context.event.get(event.name).get(eventLVKey)
                    saveEvent[eventLVKey] = eventItem

        saveAlarm = {}
        if alarm is not None:
            for alarmLVKey in alarm.getAlarmLVs().keys():
                if alarm.getAlarmLVs().get(alarmLVKey).isSave:
                    alarmItem = context.alarm.get(alarm.name).get(alarmLVKey)
                    saveAlarm[alarmLVKey] = alarmItem

        if ConditionsBasic.IsRun.value in context.conditions.keys() \
                and self.isRunStateChange(context) \
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

        if alarm is not None:
            AlarmHistory.objects.create(alarmCode=context.mp[MpBasic.AlarmCode.value],
                                        alarmName=alarm.name,
                                        eqpId=eqpModule.eqp,
                                        eqpName=eqpModule.eqpName,
                                        eqpCode=context.mp[MpBasic.EqpCode.value],
                                        eqpModuleId=eqpModule.id,
                                        eqpModuleName=eqpModule.name,
                                        updateTime=now,
                                        value=saveAlarm,
                                        context=context.get_simpleContext(),
                                        fdcDataGroup=context.currentFdcDataGroup)

        if ConditionsBasic.IsRun.value in context.conditions.keys() \
                and context.conditions[ConditionsBasic.IsRun.value]:
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

        if ConditionsBasic.IsRun.value in context.conditions.keys() \
                and self.isRunStateChange(context) and \
                not context.conditions[ConditionsBasic.IsRun.value]:
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
            if FdcDataGroup.objects.filter(_id=context.currentFdcDataGroup).count() > 0:
                fdcDataGroup = FdcDataGroup.objects.get(_id=context.currentFdcDataGroup)
                fdcDataGroup.context = context.get_simpleContext()
                fdcDataGroup.etc = context.etc
                fdcDataGroup.endTime = now
                fdcDataGroup.betweenTimeSec = (fdcDataGroup.endTime - fdcDataGroup.startTime).seconds
                fdcDataGroup.save()
                context.currentFdcDataGroup = None
            else:
                context.currentFdcDataGroup = None
