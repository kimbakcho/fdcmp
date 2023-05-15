from dataclasses import dataclass


@dataclass
class PredictParamInfoResDto:
    id: int
    eqpModule: int
    logic: str
    paramInfo: dict | str
    etcInfo: dict | str
    schedulePredictParamInfo: dict

@dataclass
class PredictParamInfoUpdateReqDto:
    id: int
    paramInfo: dict | str
    etcInfo: dict | str
    schedulePredictParamInfo: dict| str