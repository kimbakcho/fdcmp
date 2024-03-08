import logging
import traceback

from bFdcAPI.MCP.UseCase import FdcMcpUseCase
from mcp.Process.Enum import FabGroupType
from mcp.Process.MCPEqpAlarm import MCPEqpAlarm
from mcp.Process.MCPEqpEvent import MCPEqpEvent
from mcp.Process.MCPEqpModule import MCPEqpModule
from FDCContext.context import Context, MpBasic, ConditionsBasic

from datetime import datetime

from mcp.Process.MCPEqpTraceGroup import McpEqpTraceGroup
import copy

from mcp.Process.MCPThread import MCPThread
from mcp.models import EventHistory, FdcDataGroup, TraceData, AlarmHistory, SPCData


class McpWorker:

    def __init__(self, context: Context,eqpModule: MCPEqpModule) -> None:
        super().__init__()
        self.__maxHistorySize = 20
        self.__logger = logging.getLogger('mcp')
        self.context = context
        self.eqpModule = eqpModule
        self.threadingMap: dict[str,MCPThread] = dict()
        self.initThreading()

    def __del__(self):
        for key in list(self.threadingMap.keys()):
            pop = self.threadingMap.pop(key)
            pop.stop()

    def initThreading(self):
        for key in list(self.threadingMap.keys()):
            pop = self.threadingMap.pop(key)
            pop.stop()
        items = FdcMcpUseCase.getThreadingLoops(self.eqpModule.id)
        for item in items:
            if item.logicCode is not None:
                mcp_thread = MCPThread(self.context, item)
                self.threadingMap[item.name] = mcp_thread
                self.threadingMap[item.name].startLoop()

    def createOrUpdateThreading(self, threadLoopId: int):
        threadLoop = FdcMcpUseCase.getThreadingLoop(threadLoopId)
        if threadLoop.name in list(self.threadingMap.keys()):
            popItem = self.threadingMap.pop(threadLoop.name)
            popItem.stop()

        if threadLoop.logicCode is not None:
            mcp_thread = MCPThread(self.context, threadLoop)
            self.threadingMap[threadLoop.name] = mcp_thread
            self.threadingMap[threadLoop.name].startLoop()

    def deleteThreading(self, threadLoopName: str):

        if threadLoopName in list(self.threadingMap.keys()):
            popItem = self.threadingMap.pop(threadLoopName)
            popItem.stop()

    def run(self):
        try:
            event = None
            traceGroup = None
            alarm = None
            if self.context.mp.get(MpBasic.IsEvent.value, None) \
                    and self.context.mp[MpBasic.EventCode.value] in self.eqpModule.getEvents().keys():
                event = self.eqpModule.getEvents()[self.context.mp[MpBasic.EventCode.value]]
                for logicItem in event.getLogics(event.id):
                    try:
                        exec(logicItem.logicComPile, None, locals())
                        runResult = locals().get("run")(self.context)
                        if event.name not in self.context.event.keys():
                            self.context.event[event.name] = {}
                        self.context.event[event.name][logicItem.name] = runResult
                    except Exception as e:
                        self.__logger.error(self.context.get_message())
                        self.__logger.error(f'{self.eqpModule.eqpName}_{self.eqpModule.name} {logicItem.name}')
                        self.__logger.error(traceback.format_exc())
                        self.__logger.error(e.__str__())
                        self.__logger.error(traceback.format_stack())
                        traceback.print_stack()

            if self.context.mp.get(MpBasic.IsAlarm.value, None) \
                    and self.context.mp[MpBasic.AlarmCode.value] in self.eqpModule.getAlarms().keys():
                alarm = self.eqpModule.getAlarms()[self.context.mp[MpBasic.AlarmCode.value]]
                for logicItem in alarm.getLogics(alarm.id):
                    try:
                        exec(logicItem.logicComPile, None, locals())
                        runResult = locals().get("run")(self.context)
                        if alarm.name not in self.context.alarm.keys():
                            self.context.alarm[alarm.name] = {}
                        self.context.alarm[alarm.name][logicItem.name] = runResult
                    except Exception as e:
                        self.__logger.error(self.context.get_message())
                        self.__logger.error(f'{self.eqpModule.eqpName}_{self.eqpModule.name} {logicItem.name}')
                        self.__logger.error(traceback.format_exc())
                        self.__logger.error(e.__str__())
                        self.__logger.error(traceback.format_stack())
                        traceback.print_stack()

            if self.context.mp.get(MpBasic.IsTrace.value, None) \
                    and self.context.mp[MpBasic.TraceGroupCode.value] in self.eqpModule.getTraceGroup().keys():
                traceGroup = self.eqpModule.getTraceGroup()[self.context.mp[MpBasic.TraceGroupCode.value]]
                for logicItem in traceGroup.getTraceLogic():
                    try:
                        exec(logicItem.logicComPile, None, locals())
                        runResult = locals().get("run")(self.context)
                        if traceGroup.name not in self.context.trace.keys():
                            self.context.trace[traceGroup.name] = {}
                        self.context.trace[traceGroup.name][logicItem.name] = runResult
                    except Exception as e:
                        self.__logger.error(self.context.get_message())
                        self.__logger.error(f'{self.eqpModule.eqpName}_{self.eqpModule.name} {logicItem.name}')
                        self.__logger.error(traceback.format_exc())
                        self.__logger.error(e.__str__())
                        self.__logger.error(traceback.format_stack())
                        traceback.print_stack()

            for conditions in self.eqpModule.getConditions():
                try:
                    exec(conditions.logicComPile, None, locals())
                    runResult = locals().get("run")(self.context)
                    self.context.conditions[conditions.name] = runResult
                except Exception as e:
                    self.__logger.error(self.context.get_message())
                    self.__logger.error(f'{self.eqpModule.eqpName}_{self.eqpModule.name} {conditions.name}')
                    self.__logger.error(traceback.format_exc())
                    self.__logger.error(e.__str__())
                    self.__logger.error(traceback.format_stack())
                    traceback.print_stack()
            if self.context.contextHistory.__len__() >= self.__maxHistorySize:
                self.context.contextHistory.pop(0)
            self.mcpSaveWork(self.eqpModule, self.context, event, alarm, traceGroup)

            saveContext = Context()
            saveContext.mp = self.context.mp
            saveContext.event = self.context.event
            saveContext.alarm = self.context.alarm
            saveContext.trace = self.context.trace
            saveContext.spc = self.context.spc
            saveContext.etc = self.context.etc
            saveContext.conditions = self.context.conditions
            saveContext.currentFdcDataGroup = self.context.currentFdcDataGroup

            self.context.contextHistory.append(copy.deepcopy(saveContext))
        except Exception as e:
            logger = logging.getLogger('mcp')
            logger.error(self.context.get_message())
            self.__logger.error(f'{self.eqpModule.eqpName}_{self.eqpModule.name}')
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

        now = datetime.now()
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
                                        eqpModuleCode=eqpModule.code,
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
                                        eqpModuleCode=eqpModule.code,
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
                    eqpModuleCode=eqpModule.code,
                    eqpModuleName=eqpModule.name,
                    context=context.get_simpleContext(),
                    updateTime=now,
                    fdcDataGroup=context.currentFdcDataGroup
                )

        if context.getSPCData() is not None:
            SPCData.objects.create(
                value=context.getSPCData(),
                eqpId=eqpModule.eqp,
                eqpName=eqpModule.eqpName,
                eqpCode=context.mp[MpBasic.EqpCode.value],
                eqpModuleId=eqpModule.id,
                eqpModuleCode=eqpModule.code,
                eqpModuleName=eqpModule.name,
                context=context.get_simpleContext(),
                updateTime=now,
                fdcDataGroup=context.currentFdcDataGroup
            )
            context.setSPCData(None)

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
            eqpModuleCode=eqpModule.code,
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
                fdcDataGroup.betweenTimeSec = int((fdcDataGroup.endTime - fdcDataGroup.startTime).total_seconds())
                fdcDataGroup.save()
                context.currentFdcDataGroup = None
            else:
                context.currentFdcDataGroup = None
