import logging
import sys

from django.apps import AppConfig


class MplConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mpl'

    def ready(self):
        if 'runserver' in sys.argv or 'fdcmp.wsgi' in sys.argv or 'fdcmp.asgi' in sys.argv:
            logging.getLogger("mpl").info("startService")
            from mpl.Process.MPLProcessWorker import mplProcessWorker
            mplProcessWorker()
