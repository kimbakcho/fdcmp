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

from bFdcAPI.Eqp.Dto.FdcEqpModule import FdcEqpModuleResDto
from bFdcAPI.Eqp.UseCase import FdcEqpUseCase


class CapaSchedulerWorker:

    def __init__(self, module: FdcEqpModuleResDto) -> None:
        self.module = module
        super().__init__()

    def start(self):
        lists = CapaUseCase.getTrainSchedulerHistoryList(TrainSchedulerHistoryListReqDto(execute=False,
                                                                                         trainScheduler__eqpModule=self.module.id,
                                                                                         planTime__lte=datetime.now().isoformat()))


        if lists.__len__() > 0:
            trainValidData = CapaUseCase.getTrainValidData(self.module.id)
            trainValidDataContext = TrainValidDataContext()
            trainValidDataContext.setEqpCode(self.module.eqpCode)
            trainValidDataContext.setEqpName(self.module.eqpName)
            trainValidDataContext.setEqpModuleCode(self.module.code)
            trainValidDataContext.setEqpModuleName(self.module.name)
            if trainValidData.logicCode is not None and trainValidData.logicCode.__len__() > 0:
                try:
                    com = compile(decoratorLogicCode(trainValidData.logicCode), '<string>', mode='exec')
                    exec(com, None, locals())
                    runResult = locals().get("run")(trainValidDataContext)
                    trainValidDataContext.trainValidData = runResult
                    reqDto = TrainValidDataUpdateReqDto(id=trainValidData.id,
                                                        trainData=json.dumps(trainValidDataContext.getTrainData()),
                                                        validData=json.dumps(trainValidDataContext.getValidData()),
                                                        trainPeriodStart=trainValidDataContext.getTrainPeriodStart(),
                                                        trainPeriodEnd=trainValidDataContext.getTrainPeriodEnd())
                    CapaUseCase.updateTrainValidData(reqDto)
                except Exception as e:
                    logging.getLogger("capa").error(f'{self.module.eqpName}_{self.module.name}')
                    logging.getLogger("capa").error(traceback.format_exc())
                    logging.getLogger("capa").error(e.__str__())
                    logging.getLogger("capa").error(traceback.format_stack())
                    traceback.print_stack()

            trainLogic = CapaUseCase.getTrainLogic(self.module.id)
            trainLogicContext = None
            if trainLogic.logic is not None and trainLogic.logic.__len__() > 0:
                trainLogicContext = TrainLogicContext(self.module.id)
                trainLogicContext.setEqpCode(self.module.eqpCode)
                trainLogicContext.setEqpName(self.module.eqpName)
                trainLogicContext.setEqpModuleCode(self.module.code)
                trainLogicContext.setEqpModuleName(self.module.name)
                try:
                    com = compile(decoratorLogicCode(trainLogic.logic), '<string>', mode='exec')
                    exec(com, None, locals())
                    locals().get("run")(trainLogicContext)
                    trainModels = trainLogicContext.getTrainModels()
                    saveJson = self._getTrainModelToDict(trainModels)
                    trainedInfo = trainLogicContext.getTrainedInfo()
                    CapaUseCase.updateTrainLogic(
                        TrainLogicUpdateReqDto(id=trainLogic.id, trainedModel=json.dumps(saveJson), trainedInfo=json.dumps(trainedInfo)))
                except Exception as e:
                    logging.getLogger("capa").error(f'{self.module.eqpName}_{self.module.name}')
                    logging.getLogger("capa").error(traceback.format_exc())
                    logging.getLogger("capa").error(e.__str__())
                    logging.getLogger("capa").error(traceback.format_stack())
                    traceback.print_stack()

            predictParamInfo = CapaUseCase.getPredictParamInfo(self.module.id)
            predictParamInfoContext = None
            if predictParamInfo.logic is not None and predictParamInfo.logic.__len__() > 0:
                predictParamInfoContext = PredictParamInfoContext(self.module.id)
                predictParamInfoContext.setEqpCode(self.module.eqpCode)
                predictParamInfoContext.setEqpName(self.module.eqpName)
                predictParamInfoContext.setEqpModuleCode(self.module.code)
                predictParamInfoContext.setEqpModuleName(self.module.name)
                try:
                    com = compile(decoratorLogicCode(predictParamInfo.logic), '<string>', mode='exec')
                    exec(com, None, locals())
                    locals().get("run")(predictParamInfoContext)
                    CapaUseCase.updatePredictParamInfo(PredictParamInfoUpdateReqDto(id=predictParamInfo.id,
                                                                                    paramInfo=json.dumps(
                                                                                        predictParamInfoContext.getPredictParamInfo()),
                                                                                    etcInfo=json.dumps(
                                                                                        predictParamInfoContext.getPredictEtcInfo()),
                                                                                    schedulePredictParamInfo=json.dumps(
                                                                                        predictParamInfoContext.getSchedulePredictParamInfo())))

                except Exception as e:
                    logging.getLogger("capa").error(f'{self.module.eqpName}_{self.module.name}')
                    logging.getLogger("capa").error(traceback.format_exc())
                    logging.getLogger("capa").error(e.__str__())
                    logging.getLogger("capa").error(traceback.format_stack())
                    traceback.print_stack()

            predictResults = list()

            predictLogic = CapaUseCase.getPredictLogic(self.module.id)
            predictLogicContext = None
            if predictParamInfo.schedulePredictParamInfo is not None and predictParamInfo.logic.__len__() > 0:
                if predictLogic.logic is not None and predictLogic.logic.__len__() > 0:
                    predictLogicContext = PredictLogicContext(self.module.id)
                    predictLogicContext.setEqpCode(self.module.eqpCode)
                    predictLogicContext.setEqpName(self.module.eqpName)
                    predictLogicContext.setEqpModuleCode(self.module.code)
                    predictLogicContext.setEqpModuleName(self.module.name)
                    try:
                        com = compile(decoratorLogicCode(predictLogic.logic), '<string>', mode='exec')
                        exec(com, None, locals())
                        for schedulerItem in predictParamInfo.schedulePredictParamInfo:
                            predictLogicContext.setPredictParams(schedulerItem)
                            locals().get("run")(predictLogicContext)
                            predictResults.append({
                                "predictParams": schedulerItem,
                                "predictResult": predictLogicContext.getPredictResult()})

                    except Exception as e:
                        logging.getLogger("capa").error(f'{self.module.eqpName}_{self.module.name}')
                        logging.getLogger("capa").error(traceback.format_exc())
                        logging.getLogger("capa").error(e.__str__())
                        logging.getLogger("capa").error(traceback.format_stack())
                        traceback.print_stack()

            for item in lists:
                CapaUseCase.updateTrainSchedulerHistory(TrainSchedulerHistoryUpdateReqDto(id=item.id, execute=True,
                                                                                          executeTime=datetime.now().isoformat(),
                                                                                          predictResult=json.dumps(predictResults),
                                                                                          trainedModel=None,
                                                                                          paramInfo=None))
                if trainLogicContext is not None:
                    trainModels = trainLogicContext.getTrainModels()
                    saveJson = self._getTrainModelToDict(trainModels)
                    if saveJson is not None:
                        CapaUseCase.updateTrainSchedulerHistory(
                            TrainSchedulerHistoryUpdateReqDto(id=item.id, execute=None,
                                                              executeTime=None,
                                                              predictResult=None,
                                                              trainedModel=json.dumps(saveJson),
                                                              paramInfo=None))
                if predictParamInfoContext is not None and predictParamInfoContext.getSchedulePredictParamInfo() is not None:
                    CapaUseCase.updateTrainSchedulerHistory(
                        TrainSchedulerHistoryUpdateReqDto(id=item.id, execute=None,
                                                          executeTime=None,
                                                          predictResult=None,
                                                          trainedModel=None,
                                                          paramInfo=json.dumps(predictParamInfoContext.getSchedulePredictParamInfo())))


    def _getTrainModelToDict(self, trainModels) -> dict | None:
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
            return saveJson
        return None
