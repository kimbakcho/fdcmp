import logging
import sys
import traceback

from django.apps import AppConfig

from bFdcEqp.Dto.FdcEqpReqDto import FdcEqpReqDto
from bFdcEqp.views import FdcEqpUseCase
from init.eqpInIt import EqpInit
import environ

env = environ.Env()

initEqpLogger = logging.getLogger("initEqp")


class InitConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'init'
    eqpInitMap = {}

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        try:
            fdcEqpUseCase = FdcEqpUseCase()
            eqps = fdcEqpUseCase.getEqpList(FdcEqpReqDto(core=env('MP_CORE_ID')))
            eqpInitList = list(map(lambda eqp: EqpInit(eqp), eqps))
            eqpInitMap = {eqpInit.eqpId: eqpInit for eqpInit in eqpInitList}
        except Exception as e:
            initEqpLogger.error(e.__str__())
            initEqpLogger.error(traceback.print_stack())
