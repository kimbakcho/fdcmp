from datetime import datetime

from bFdcAPI.Capa.Dto.TrainSchedulerHistory import TrainSchedulerHistoryListReqDto
from bFdcAPI.Capa.UseCase import CapaUseCase


class CapaSchedulerWorker:

    def __init__(self,moduleId: int) -> None:
        self.moduleId = moduleId
        super().__init__()

    def start(self):
        lists = CapaUseCase.getTrainSchedulerHistoryList(TrainSchedulerHistoryListReqDto(execute=False,
                                                                                         trainScheduler__eqpModule=self.moduleId,
                                                                                         planTime__lte=datetime.now().isoformat()))
