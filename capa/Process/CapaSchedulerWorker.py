import logging
import pickle
import traceback
from datetime import datetime

from CapaContext.CapaContextImpl import TrainValidDataContext, TrainLogicContext, PredictParamInfoContext, \
    PredictLogicContext
from FDCContext.logicConverter import decoratorLogicCode
from bFdcAPI.Capa.Dto.PredictParamInfo import PredictParamInfoUpdateReqDto
from bFdcAPI.Capa.Dto.TrainLogic import TrainLogicUpdateReqDto
from bFdcAPI.Capa.Dto.TrainSchedulerHistory import TrainSchedulerHistoryListReqDto
from bFdcAPI.Capa.Dto.TrainValidData import TrainValidDataUpdateReqDto
from bFdcAPI.Capa.UseCase import CapaUseCase

from bFdcAPI.Eqp.Dto.FdcEqpModule import FdcEqpModuleResDto


class CapaSchedulerWorker:

    @staticmethod
    def start(module: FdcEqpModuleResDto,schedulerHistoryId: int):
        logging.getLogger("capa").info(f"{module.eqpName} Capa Train Start")
        trainValidData = CapaUseCase.getTrainValidData(module.id)
        trainValidDataContext = TrainValidDataContext()
        trainValidDataContext.setEqpCode(module.eqpCode)
        trainValidDataContext.setEqpName(module.eqpName)
        trainValidDataContext.setEqpModuleCode(module.code)
        trainValidDataContext.setEqpModuleName(module.name)
        if trainValidData.logicCode is not None and trainValidData.logicCode.__len__() > 0:
            try:
                logging.getLogger("capa").info(f"{module.eqpName} Capa trainValidData Start")
                com = compile(decoratorLogicCode(trainValidData.logicCode), '<string>', mode='exec')
                exec(com, None, locals())
                runResult = locals().get("run")(trainValidDataContext)
                trainValidDataContext.trainValidData = runResult
                reqDto = TrainValidDataUpdateReqDto(id=trainValidData.id,
                                                    trainData=trainValidDataContext.getTrainData(),
                                                    validData=trainValidDataContext.getValidData(),
                                                    trainPeriodStart=trainValidDataContext.getTrainPeriodStart().isoformat(),
                                                    trainPeriodEnd=trainValidDataContext.getTrainPeriodEnd().isoformat())
                CapaUseCase.saveTrainValidData(reqDto)
                logging.getLogger("capa").info(f"{module.eqpName} Capa trainValidData End")
            except Exception as e:
                logging.getLogger("capa").error(f'{module.eqpName}_{module.name}')
                logging.getLogger("capa").error(traceback.format_exc())
                logging.getLogger("capa").error(e.__str__())
                logging.getLogger("capa").error(traceback.format_stack())
                traceback.print_stack()

        trainLogic = CapaUseCase.getTrainLogic(module.id)
        trainLogicContext = None
        if trainLogic.logic is not None and trainLogic.logic.__len__() > 0:
            trainLogicContext = TrainLogicContext(module.id)
            trainLogicContext.setEqpCode(module.eqpCode)
            trainLogicContext.setEqpName(module.eqpName)
            trainLogicContext.setEqpModuleCode(module.code)
            trainLogicContext.setEqpModuleName(module.name)
            try:
                logging.getLogger("capa").info(f"{module.eqpName} Capa trainLogic Start")
                com = compile(decoratorLogicCode(trainLogic.logic), '<string>', mode='exec')
                exec(com, None, locals())
                locals().get("run")(trainLogicContext)
                trainModels = trainLogicContext.getTrainModels()
                saveJson = CapaSchedulerWorker._getTrainModelToDict(trainModels)
                trainedInfo = trainLogicContext.getTrainedInfo()
                CapaUseCase.saveTrainLogic(
                    TrainLogicUpdateReqDto(id=trainLogic.id, trainedModel=saveJson, trainedInfo=trainedInfo))
                logging.getLogger("capa").info(f"{module.eqpName} Capa trainLogic End")
            except Exception as e:
                logging.getLogger("capa").error(f'{module.eqpName}_{module.name}')
                logging.getLogger("capa").error(traceback.format_exc())
                logging.getLogger("capa").error(e.__str__())
                logging.getLogger("capa").error(traceback.format_stack())
                traceback.print_stack()

        predictParamInfo = CapaUseCase.getPredictParamInfo(module.id)
        predictParamInfoContext = None
        if predictParamInfo.logic is not None and predictParamInfo.logic.__len__() > 0:
            predictParamInfoContext = PredictParamInfoContext(module.id)
            predictParamInfoContext.setEqpCode(module.eqpCode)
            predictParamInfoContext.setEqpName(module.eqpName)
            predictParamInfoContext.setEqpModuleCode(module.code)
            predictParamInfoContext.setEqpModuleName(module.name)
            try:
                logging.getLogger("capa").info(f"{module.eqpName} Capa predictParam Start")
                com = compile(decoratorLogicCode(predictParamInfo.logic), '<string>', mode='exec')
                exec(com, None, locals())
                locals().get("run")(predictParamInfoContext)
                CapaUseCase.savePredictParamInfo(PredictParamInfoUpdateReqDto(id=predictParamInfo.id,
                                                                              paramInfo=
                                                                              predictParamInfoContext.getPredictParamInfo(),
                                                                              etcInfo=
                                                                              predictParamInfoContext.getPredictEtcInfo(),
                                                                              schedulePredictParamInfo=
                                                                              predictParamInfoContext.getSchedulePredictParamInfo()))
                logging.getLogger("capa").info(f"{module.eqpName} Capa predictParam End")
            except Exception as e:
                logging.getLogger("capa").error(f'{module.eqpName}_{module.name}')
                logging.getLogger("capa").error(traceback.format_exc())
                logging.getLogger("capa").error(e.__str__())
                logging.getLogger("capa").error(traceback.format_stack())
                traceback.print_stack()

        # predictResults = list()
        #
        # predictLogic = CapaUseCase.getPredictLogic(self.module.id)
        # predictLogicContext = None
        # if predictParamInfo.schedulePredictParamInfo is not None and predictParamInfo.logic.__len__() > 0:
        #     if predictLogic.logic is not None and predictLogic.logic.__len__() > 0:
        #         predictLogicContext = PredictLogicContext(self.module.id)
        #         predictLogicContext.setEqpCode(self.module.eqpCode)
        #         predictLogicContext.setEqpName(self.module.eqpName)
        #         predictLogicContext.setEqpModuleCode(self.module.code)
        #         predictLogicContext.setEqpModuleName(self.module.name)
        #         try:
        #             com = compile(decoratorLogicCode(predictLogic.logic), '<string>', mode='exec')
        #             exec(com, None, locals())
        #             for schedulerItem in predictParamInfo.schedulePredictParamInfo:
        #                 predictLogicContext.setPredictParams(schedulerItem)
        #                 locals().get("run")(predictLogicContext)
        #                 predictResults.append({
        #                     "predictParams": schedulerItem,
        #                     "predictResult": predictLogicContext.getPredictResult()})
        #
        #         except Exception as e:
        #             logging.getLogger("capa").error(f'{self.module.eqpName}_{self.module.name}')
        #             logging.getLogger("capa").error(traceback.format_exc())
        #             logging.getLogger("capa").error(e.__str__())
        #             logging.getLogger("capa").error(traceback.format_stack())
        #             traceback.print_stack()
        #

        CapaUseCase.updateTrainSchedulerHistory({
            "id": schedulerHistoryId,
            "execute": True,
            "executeTime": datetime.now().isoformat(),
            "paramInfo": predictParamInfo.paramInfo,
        })
        if trainLogicContext is not None:
            trainModels = trainLogicContext.getTrainModels()
            saveJson = CapaSchedulerWorker._getTrainModelToDict(trainModels)
            if saveJson is not None:
                CapaUseCase.updateTrainSchedulerHistory({
                    "id":schedulerHistoryId,
                    "trainedModel": saveJson
                })
        CapaUseCase.setupNextScheduler(eqpModule=module.id)
        logging.getLogger("capa").info(f"{module.eqpName} Capa Train End")

    @staticmethod
    def _getTrainModelToDict(trainModels) -> dict | None:
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
