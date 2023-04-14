def decoratorLogicCode(logicCode: str):
    logicCode = logicCode.replace("\n", "\n\t")
    logicCode = "\t" + logicCode
    logicCode = "def run(context):\n" + logicCode
    logicCode = logicCode + "\n\treturn run(context)"
    return logicCode
