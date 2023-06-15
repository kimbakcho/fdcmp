from dataclasses import dataclass


@dataclass
class RecipeInterLockRecipeResDto:
    id: int
    recipeName: str
    RILOperation: int
    updateTime: str
    orderIdx: int
    useParamInterLock: bool
    paramInterLock: list
    user: int


@dataclass
class RILRecipeQuickSearchReqDto:
    eqpCode: str
    moduleCode: str
    operationCode: str
    recipeName: str