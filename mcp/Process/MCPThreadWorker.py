import logging
import traceback

from mcp.Process.MCPEqpModule import MCPEqpModule
from FDCContext.context import Context


def mcpWorker(eqpModule: MCPEqpModule, context: Context):
    logger = logging.getLogger('mcp')
    try:
        if context.mp["EventCode"] in eqpModule.getEvents().keys():
            event = eqpModule.getEvents()[context.mp["EventCode"]]
            for logicItem in event.getLogics(event.id):
                exec(logicItem.logicComPile, None, locals())
                runResult = locals().get("run")(context)
                if event.name not in context.event.keys():
                    context.event[event.name] = {}
                context.event[event.name][logicItem.name] = runResult
        if context.mp["TraceGroupCode"] in eqpModule.getTraceGroup().keys():
            traceGroup = eqpModule.getTraceGroup()[context.mp["TraceGroupCode"]]
            for logicItem in traceGroup.getTraceLogic():
                exec(logicItem.logicComPile, None, locals())
                runResult = locals().get("run")(context)
                if traceGroup.name not in context.trace.keys():
                    context.trace[traceGroup.name][logicItem.name] = {}
                context.trace[traceGroup.name][logicItem.name] = runResult
        for conditions in eqpModule.getConditions():
            exec(conditions.logicComPile, None, locals())
            runResult = locals().get("run")(context)
            context.conditions[conditions.name] = runResult
        print("done")
    except Exception as e:
        logger.error(e.__str__())
        logger.error(traceback.print_stack())
