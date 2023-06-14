import logging
import os
import sys

from django.apps import AppConfig


class AcpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'acp'
    def ready(self):
        if 'runserver' in sys.argv or 'fdcmp.wsgi' in sys.argv or 'fdcmp.asgi:application' in sys.argv:
            if 'runserver' in sys.argv:
                if not os.environ.get('RUN_MAIN'):
                    return
            logging.getLogger("acp").info("startService")

            from acp.Process.ACPProcessWorker import acpProcessWorker
            acpProcessWorker()