import logging

import time
import traceback
from environ import environ

from bFdcAPI.Capa.Dto.TrainSchedulerHistory import TrainSchedulerHistoryListReqDto
from bFdcAPI.Capa.UseCase import CapaUseCase
from bFdcAPI.Eqp.UseCase import FdcEqpUseCase
from capa.Process.CapaSchedulerWorker import CapaSchedulerWorker

from datetime import datetime
from multiprocessing import Pool

env = environ.Env()


def capaProcessWorker():
    logger = logging.getLogger("capa")
    pools = Pool(processes=env.get_value("CAPA_PROCESSES_POOL_COUNT", int))
    while True:
        try:
            schedulerList = CapaUseCase.getTrainSchedulerHistoryList(
                TrainSchedulerHistoryListReqDto(execute=False,
                                                trainScheduler__eqpModule=None,
                                                planTime__lte=datetime.now().isoformat()))
            for scheduler in schedulerList:
                module = FdcEqpUseCase.getEqpModule(scheduler.trainScheduler.eqpModule)
                CapaUseCase.updateTrainSchedulerHistory({"id": scheduler.id, "execute": True, "executeTime": datetime.now().isoformat()})
                CapaUseCase.setupNextScheduler(eqpModule=module.id)
                pools.apply_async(func=CapaSchedulerWorker.start, args=[module, scheduler.id])
            time.sleep(10)
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error(e.__str__())
            logger.error(traceback.format_stack())
            traceback.print_stack()
            time.sleep(10)
