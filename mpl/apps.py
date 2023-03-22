import sys

from django.apps import AppConfig
import stomp
from queue import Queue
import requests
import environ
from mpl.Dto.MessageParserCore import MessageParserCoreResDto
from mpl.Listener.MPLCommandListener import MPLCommandListener
from mpl.Listener.MPListener import MPListener
from mpl.Process.MPLProcessWorker import mplProcessWorker


class MplConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mpl'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        env = environ.Env()

        r = requests.get(f"{env('BFDC_URL')}/mp/core/{env('MP_CORE_ID')}/")

        coreInfo = r.json()

        c = stomp.Connection([(coreInfo["ESBIp"], coreInfo['ESBPort'])])

        c.set_listener("mp", MPListener())

        c.connect()

        c.subscribe(coreInfo["subject"], env('MP_CORE_ID'))

        m = stomp.Connection([(coreInfo["ESBIp"], coreInfo['ESBPort'])])

        m.set_listener("mpCommand", MPLCommandListener())

        m.connect()

        m.subscribe(coreInfo["commandSubject"], env('MP_CORE_ID'))


        mplProcessWorker()


