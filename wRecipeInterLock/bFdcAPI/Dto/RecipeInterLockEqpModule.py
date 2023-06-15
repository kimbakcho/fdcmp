from dataclasses import dataclass


@dataclass
class RecipeInterLockEqpModuleResDto:
    id: int
    RILEqp: int
    module: int
    moduleName: str
    orderIdx: int
    updateTime: str
    user: int


@dataclass
class RecipeInterLockEqpModuleReqDto:
    eqpCode: str
    moduleCode: str
