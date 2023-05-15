import logging
import pickle
import traceback
from datetime import datetime

from CapaContext.CapaContextImpl import TrainValidDataContext, TrainLogicContext, PredictParamInfoContext, \
    PredictLogicContext
from FDCContext.logicConverter import decoratorLogicCode
from bFdcAPI.Capa.Dto.PredictParamInfo import PredictParamInfoUpdateReqDto
from bFdcAPI.Capa.Dto.TrainLogic import TrainLogicUpdateReqDto
from bFdcAPI.Capa.Dto.TrainSchedulerHistory import TrainSchedulerHistoryListReqDto, TrainSchedulerHistoryUpdateReqDto
from bFdcAPI.Capa.Dto.TrainValidData import TrainValidDataUpdateReqDto
from bFdcAPI.Capa.UseCase import CapaUseCase
import json

class CapaSchedulerWorker:

    def __init__(self, moduleId: int) -> None:
        self.moduleId = moduleId
        super().__init__()

    def start(self):
        lists = CapaUseCase.getTrainSchedulerHistoryList(TrainSchedulerHistoryListReqDto(execute=False,
                                                                                         trainScheduler__eqpModule=self.moduleId,
                                                                                         planTime__lte=datetime.now().isoformat()))
        if lists.__len__() > 0:
            trainValidData = CapaUseCase.getTrainValidData(self.moduleId)
            context = TrainValidDataContext()
            if trainValidData.logicCode is not None and trainValidData.logicCode.__len__() > 0:
                try:
                    com = compile(decoratorLogicCode(trainValidData.logicCode), '<string>', mode='exec')
                    exec(com, None, locals())
                    runResult = locals().get("run")(context)
                    context.trainValidData = runResult
                    reqDto = TrainValidDataUpdateReqDto(id=trainValidData.id, trainData=json.dumps(context.getTrainData()),
                                                        validData=json.dumps(context.getValidData()))
                    CapaUseCase.updateTrainValidData(reqDto)
                except Exception as e:
                    logging.getLogger("capa").error(e.__str__())
                    logging.getLogger("capa").error(traceback.format_stack())
                    traceback.print_stack()

            trainLogic = CapaUseCase.getTrainLogic(self.moduleId)
            if trainLogic.logic is not None and trainLogic.logic.__len__() > 0:
                context = TrainLogicContext(self.moduleId)
                try:
                    com = compile(decoratorLogicCode(trainLogic.logic), '<string>', mode='exec')
                    exec(com, None, locals())
                    locals().get("run")(context)
                    trainModels = context.getTrainModels()
                    if trainModels is not None:
                        saveJson = {}
                        for modelName in trainModels.keys():
                            trainModel = trainModels[modelName]
                            if trainModel.type == "pickle":
                                import base64
                                saveJson[modelName] = {
                                    "type": "pickle",
                                    "model": base64.b64encode(pickle.dumps(trainModel.model)).decode("ascii")
                                }
                        CapaUseCase.updateTrainLogic(TrainLogicUpdateReqDto(id=trainLogic.id, trainedModel=json.dumps(saveJson)))
                except Exception as e:
                    logging.getLogger("capa").error(e.__str__())
                    logging.getLogger("capa").error(traceback.format_stack())
                    traceback.print_stack()

            predictParamInfo = CapaUseCase.getPredictParamInfo(self.moduleId)
            if predictParamInfo.logic is not None and predictParamInfo.logic.__len__() > 0:
                context = PredictParamInfoContext(self.moduleId)
                try:
                    com = compile(decoratorLogicCode(predictParamInfo.logic), '<string>', mode='exec')
                    exec(com, None, locals())
                    locals().get("run")(context)
                    CapaUseCase.updatePredictParamInfo(PredictParamInfoUpdateReqDto(id=predictParamInfo.id,
                                                                                    paramInfo=json.dumps(context.getPredictParamInfo()),
                                                                                    etcInfo=json.dumps(context.getPredictEtcInfo()),
                                                                                    schedulePredictParamInfo=json.dumps(context.getSchedulePredictParamInfo())))

                except Exception as e:
                    logging.getLogger("capa").error(e.__str__())
                    logging.getLogger("capa").error(traceback.format_stack())
                    traceback.print_stack()

            predictResults = list()

            predictLogic = CapaUseCase.getPredictLogic(self.moduleId)
            if predictParamInfo.schedulePredictParamInfo is not None and predictParamInfo.logic.__len__() > 0:
                if predictLogic.logic is not None and predictLogic.logic.__len__() > 0:
                    context = PredictLogicContext(self.moduleId)
                    try:
                        com = compile(decoratorLogicCode(predictLogic.logic), '<string>', mode='exec')
                        exec(com, None, locals())
                        for schedulerItem in predictParamInfo.schedulePredictParamInfo:
                            context.setPredictParams(schedulerItem)
                            locals().get("run")(context)
                            predictResults.append({
                                "predictParams": schedulerItem,
                                "predictResult": context.getPredictResult()})
                    except Exception as e:
                        logging.getLogger("capa").error(e.__str__())
                        logging.getLogger("capa").error(traceback.format_stack())
                        traceback.print_stack()


            for item in lists:
                CapaUseCase.updateTrainSchedulerHistory(TrainSchedulerHistoryUpdateReqDto(id=item.id, execute=True, executeTime=datetime.now().isoformat()))