import sys

from django.apps import AppConfig
from mpl.Process.MPLProcessWorker import mplProcessWorker
class MplConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mpl'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        mplProcessWorker()
